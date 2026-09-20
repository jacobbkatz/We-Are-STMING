/* The instrument, part by part: the 23 printed parts from CAD/prints/, packed by
 * build_model.py. Plain WebGL2, no library.
 *
 * Shapes and sizes are real. POSITIONS ARE AN ARRANGEMENT, not an assembly - the
 * STLs are laid out for a print bed and we do not hold the assembly transforms.
 */
(function () {
  "use strict";

  var host = document.getElementById("viewer");
  if (!host) { return; }
  var canvas = host.querySelector("canvas");
  var panel = document.getElementById("partinfo");
  var status = document.getElementById("viewstatus");

  function fail(msg) {
    host.classList.add("failed");
    if (status) { status.textContent = msg; }
  }

  var gl = canvas.getContext("webgl2", { antialias: true, alpha: true });
  if (!gl) { fail("This browser cannot draw the 3D model. Every part is still in the repository as an STL file."); return; }

  /* ---------------------------------------------------------------- shaders */
  var VS = [
    "#version 300 es",
    "in vec3 p;",
    "uniform mat4 mvp; uniform mat4 mv;",
    "uniform vec3 off; uniform float scl;",
    "out vec3 vpos;",
    "void main(){",
    "  vec3 w = p * scl + off;",
    "  vpos = (mv * vec4(w,1.0)).xyz;",
    "  gl_Position = mvp * vec4(w,1.0);",
    "}"
  ].join("\n");

  var FS = [
    "#version 300 es",
    "precision highp float;",
    "in vec3 vpos;",
    "uniform vec3 tint;",
    "out vec4 frag;",
    "void main(){",
    // face normal from derivatives, so the buffer carries no normals
    "  vec3 n = normalize(cross(dFdx(vpos), dFdy(vpos)));",
    "  if(!gl_FrontFacing) n = -n;",
    "  float key  = max(dot(n, normalize(vec3(0.45,0.75,0.55))), 0.0);",
    "  float fill = max(dot(n, normalize(vec3(-0.6,0.15,0.35))), 0.0);",
    "  float rim  = pow(1.0 - max(dot(n, vec3(0.0,0.0,1.0)), 0.0), 2.2);",
    "  vec3 c = tint * (0.30 + 0.72*key + 0.20*fill) + vec3(0.16)*rim;",
    "  frag = vec4(c, 1.0);",
    "}"
  ].join("\n");

  var PICK_FS = [
    "#version 300 es",
    "precision highp float;",
    "in vec3 vpos;",
    "uniform vec3 tint;",
    "out vec4 frag;",
    "void main(){ frag = vec4(tint, 1.0); }"
  ].join("\n");

  function shader(type, src) {
    var s = gl.createShader(type);
    gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      throw new Error(gl.getShaderInfoLog(s));
    }
    return s;
  }
  function program(fs) {
    var p = gl.createProgram();
    gl.attachShader(p, shader(gl.VERTEX_SHADER, VS));
    gl.attachShader(p, shader(gl.FRAGMENT_SHADER, fs));
    gl.bindAttribLocation(p, 0, "p");
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) { throw new Error(gl.getProgramInfoLog(p)); }
    return {
      p: p,
      mvp: gl.getUniformLocation(p, "mvp"), mv: gl.getUniformLocation(p, "mv"),
      off: gl.getUniformLocation(p, "off"), scl: gl.getUniformLocation(p, "scl"),
      tint: gl.getUniformLocation(p, "tint"), ghost: gl.getUniformLocation(p, "ghost")
    };
  }

  var draw, pick;
  try { draw = program(FS); pick = program(PICK_FS); }
  catch (e) { fail("This browser could not start the 3D view. Every part is still in the repository as an STL file."); return; }

  /* ------------------------------------------------------------ small maths */
  function mul(a, b) {
    var o = new Float32Array(16);
    for (var i = 0; i < 4; i++) for (var j = 0; j < 4; j++) {
      var s = 0; for (var k = 0; k < 4; k++) { s += a[k * 4 + j] * b[i * 4 + k]; }
      o[i * 4 + j] = s;
    }
    return o;
  }
  function perspective(fovy, asp, n, f) {
    var t = 1 / Math.tan(fovy / 2);
    return new Float32Array([t / asp,0,0,0, 0,t,0,0, 0,0,(f+n)/(n-f),-1, 0,0,2*f*n/(n-f),0]);
  }
  function lookAt(e, c, up) {
    function sub(a,b){return [a[0]-b[0],a[1]-b[1],a[2]-b[2]];}
    function norm(a){var l=Math.hypot(a[0],a[1],a[2])||1;return [a[0]/l,a[1]/l,a[2]/l];}
    function cross(a,b){return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];}
    function dot(a,b){return a[0]*b[0]+a[1]*b[1]+a[2]*b[2];}
    var z = norm(sub(e,c)), x = norm(cross(up,z)), y = cross(z,x);
    return new Float32Array([x[0],y[0],z[0],0, x[1],y[1],z[1],0, x[2],y[2],z[2],0,
                             -dot(x,e),-dot(y,e),-dot(z,e),1]);
  }

  /* ------------------------------------------------------------- the scene */
  var GROUPS = {
    "scan-head": { label: "The scan head",  tint: [0.83,0.66,0.31] },
    "isolation": { label: "The frame and suspension", tint: [0.42,0.47,0.50] }
  };
  var parts = [], radius = 1, centre = [0,0,0];
  var az = 0.58, el = 0.52, dist = 1, hover = -1, sel = -1;
  var groupOn = { "scan-head": true, "isolation": true };

  function layout(meta) {
    var order = { "scan-head": 0, "isolation": 1 };
    meta.sort(function (a, b) {
      if (order[a.group] !== order[b.group]) { return order[a.group] - order[b.group]; }
      return (b.size[0] * b.size[2]) - (a.size[0] * a.size[2]);
    });
    var cell = 0;
    meta.forEach(function (m) { cell = Math.max(cell, m.size[0], m.size[2]); });
    cell *= 1.18;
    var cols = Math.min(4, meta.length), rows = Math.ceil(meta.length / cols);
    var lo = [1e9, 0, 1e9], hi = [-1e9, 0, -1e9];
    meta.forEach(function (m, i) {
      var cx = i % cols, cz = Math.floor(i / cols);
      m.pos = [(cx - (cols - 1) / 2) * cell, m.size[1] / 2, (cz - (rows - 1) / 2) * cell];
      lo[0] = Math.min(lo[0], m.pos[0] - m.size[0] / 2);
      hi[0] = Math.max(hi[0], m.pos[0] + m.size[0] / 2);
      lo[2] = Math.min(lo[2], m.pos[2] - m.size[2] / 2);
      hi[2] = Math.max(hi[2], m.pos[2] + m.size[2] / 2);
      hi[1] = Math.max(hi[1], m.size[1]);
    });
    // Frame what is actually there, not the nominal grid: one large part next to a
    // small one makes the grid much wider than the parts fill.
    centre = [(lo[0] + hi[0]) / 2, hi[1] * 0.3, (lo[2] + hi[2]) / 2];
    radius = 0.5 * Math.max(hi[0] - lo[0], hi[2] - lo[2], hi[1]);
    dist = radius * 2.6;
  }

  function upload(meta, buf) {
    meta.forEach(function (m) {
      var view = new Int16Array(buf, m.offset * 6, m.count * 3);
      var vao = gl.createVertexArray();
      gl.bindVertexArray(vao);
      var vb = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, vb);
      gl.bufferData(gl.ARRAY_BUFFER, view, gl.STATIC_DRAW);
      gl.enableVertexAttribArray(0);
      gl.vertexAttribPointer(0, 3, gl.SHORT, false, 0, 0);
      gl.bindVertexArray(null);
      m.vao = vao;
      parts.push(m);
    });
  }

  /* --------------------------------------------------------------- drawing */
  var pickFbo = null, pickTex = null, pickDepth = null, pickW = 0, pickH = 0;
  function ensurePick(w, h) {
    if (pickFbo && pickW === w && pickH === h) { return; }
    if (pickFbo) { gl.deleteFramebuffer(pickFbo); gl.deleteTexture(pickTex); gl.deleteRenderbuffer(pickDepth); }
    pickW = w; pickH = h;
    pickTex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, pickTex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, w, h, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    pickDepth = gl.createRenderbuffer();
    gl.bindRenderbuffer(gl.RENDERBUFFER, pickDepth);
    gl.renderbufferStorage(gl.RENDERBUFFER, gl.DEPTH_COMPONENT16, w, h);
    pickFbo = gl.createFramebuffer();
    gl.bindFramebuffer(gl.FRAMEBUFFER, pickFbo);
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, pickTex, 0);
    gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, pickDepth);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  }

  function matrices(w, h) {
    var eye = [centre[0] + dist * Math.cos(el) * Math.sin(az),
               centre[1] + dist * Math.sin(el),
               centre[2] + dist * Math.cos(el) * Math.cos(az)];
    var view = lookAt(eye, centre, [0, 1, 0]);
    var proj = perspective(0.72, w / h, radius * 0.05, dist + radius * 6);
    return { mv: view, mvp: mul(proj, view) };
  }

  function render(prog, m, picking) {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = Math.max(1, Math.round(canvas.clientWidth * dpr));
    var h = Math.max(1, Math.round(canvas.clientHeight * dpr));
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
    gl.viewport(0, 0, w, h);
    gl.enable(gl.DEPTH_TEST);
    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.useProgram(prog.p);
    gl.uniformMatrix4fv(prog.mvp, false, m.mvp);
    gl.uniformMatrix4fv(prog.mv, false, m.mv);
    parts.forEach(function (pt, i) {
      if (!groupOn[pt.group]) { return; }
      var tint;
      if (picking) {
        tint = [((i + 1) & 255) / 255, (((i + 1) >> 8) & 255) / 255, 0];
      } else {
        var base = GROUPS[pt.group].tint;
        var lit = (i === sel) ? 1.0 : (i === hover ? 0.55 : 0.0);
        tint = [base[0] + (0.94 - base[0]) * lit,
                base[1] + (0.78 - base[1]) * lit,
                base[2] + (0.36 - base[2]) * lit];
        if (sel >= 0 && i !== sel) {
          var g = (tint[0] + tint[1] + tint[2]) / 3.0;
          tint = [g * 0.55 + 0.42, g * 0.55 + 0.42, g * 0.55 + 0.42];
        }
      }
      gl.uniform3f(prog.tint, tint[0], tint[1], tint[2]);
      gl.uniform3f(prog.off, pt.pos[0] - 0, pt.pos[1] - 0, pt.pos[2] - 0);
      gl.uniform1f(prog.scl, pt.scale);
      gl.bindVertexArray(pt.vao);
      gl.drawArrays(gl.TRIANGLES, 0, pt.count);
    });
    gl.bindVertexArray(null);
  }

  var need = true;
  function frame() {
    if (need) {
      need = false;
      var w = canvas.clientWidth, h = canvas.clientHeight;
      if (w > 0 && h > 0) {
        gl.disable(gl.BLEND);
        render(draw, matrices(w, h), false);
      }
    }
    requestAnimationFrame(frame);
  }
  function invalidate() { need = true; }

  function partAt(cx, cy) {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = Math.max(1, Math.round(canvas.clientWidth * dpr));
    var h = Math.max(1, Math.round(canvas.clientHeight * dpr));
    ensurePick(w, h);
    gl.bindFramebuffer(gl.FRAMEBUFFER, pickFbo);
    render(pick, matrices(canvas.clientWidth, canvas.clientHeight), true);
    var px = new Uint8Array(4);
    gl.readPixels(Math.round(cx * dpr), Math.round((canvas.clientHeight - cy) * dpr),
                  1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    var id = px[0] + (px[1] << 8);
    invalidate();
    return id > 0 ? id - 1 : -1;
  }

  /* ---------------------------------------------------------------- panel */
  function show(i) {
    if (!panel) { return; }
    if (i < 0) {
      panel.innerHTML = '<p class="hint">Drag to turn it round, scroll to zoom, and click any part for its real measurements.</p>';
      return;
    }
    var m = parts[i];
    panel.innerHTML =
      '<h4>' + m.name + '</h4>' +
      '<p class="grp">' + GROUPS[m.group].label + '</p>' +
      '<p>' + m.about + '</p>' +
      '<dl><dt>Size</dt><dd>' + m.size[0] + ' &times; ' + m.size[1] + ' &times; ' + m.size[2] + ' mm</dd>' +
      '<dt>Mesh</dt><dd>' + m.tris.toLocaleString() + ' triangles</dd>' +
      '<dt>File</dt><dd><a href="https://github.com/jacobbkatz/We-Are-STMING/blob/main/' + m.file + '">' + m.file + '</a></dd></dl>';
  }

  /* --------------------------------------------------------------- input */
  var drag = null;
  canvas.addEventListener("pointerdown", function (e) {
    canvas.setPointerCapture(e.pointerId);
    drag = { x: e.clientX, y: e.clientY, az: az, el: el, moved: 0 };
  });
  canvas.addEventListener("pointermove", function (e) {
    var r = canvas.getBoundingClientRect();
    if (drag) {
      var dx = e.clientX - drag.x, dy = e.clientY - drag.y;
      drag.moved = Math.max(drag.moved, Math.abs(dx) + Math.abs(dy));
      az = drag.az - dx * 0.008;
      el = Math.max(-1.35, Math.min(1.35, drag.el + dy * 0.008));
      invalidate();
      return;
    }
    var h = partAt(e.clientX - r.left, e.clientY - r.top);
    if (h !== hover) { hover = h; canvas.style.cursor = h >= 0 ? "pointer" : "grab"; invalidate(); }
  });
  canvas.addEventListener("pointerup", function (e) {
    var r = canvas.getBoundingClientRect();
    var wasDrag = drag && drag.moved > 5;
    drag = null;
    if (wasDrag) { return; }
    var h = partAt(e.clientX - r.left, e.clientY - r.top);
    sel = (h === sel) ? -1 : h;
    show(sel); invalidate();
  });
  canvas.addEventListener("pointercancel", function () { drag = null; });
  canvas.addEventListener("wheel", function (e) {
    e.preventDefault();
    dist = Math.max(radius * 1.1, Math.min(radius * 7, dist * (1 + Math.sign(e.deltaY) * 0.12)));
    invalidate();
  }, { passive: false });

  canvas.addEventListener("keydown", function (e) {
    var step = 0.12;
    if (e.key === "ArrowLeft")  { az -= step; }
    else if (e.key === "ArrowRight") { az += step; }
    else if (e.key === "ArrowUp")    { el = Math.min(1.35, el + step); }
    else if (e.key === "ArrowDown")  { el = Math.max(-1.35, el - step); }
    else if (e.key === "+" || e.key === "=") { dist = Math.max(radius * 1.1, dist * 0.88); }
    else if (e.key === "-")  { dist = Math.min(radius * 7, dist * 1.12); }
    else { return; }
    e.preventDefault(); invalidate();
  });

  host.querySelectorAll("[data-group]").forEach(function (b) {
    b.addEventListener("click", function () {
      var g = b.getAttribute("data-group");
      groupOn[g] = !groupOn[g];
      b.setAttribute("aria-pressed", groupOn[g] ? "true" : "false");
      if (sel >= 0 && !groupOn[parts[sel].group]) { sel = -1; show(-1); }
      invalidate();
    });
  });
  var reset = document.getElementById("viewreset");
  if (reset) {
    reset.addEventListener("click", function () {
      az = 0.58; el = 0.52; dist = radius * 2.6; sel = -1; show(-1); invalidate();
    });
  }
  window.addEventListener("resize", invalidate, { passive: true });

  /* ----------------------------------------------------------------- load */
  fetch("model/parts.json").then(function (r) { return r.json(); }).then(function (doc) {
    // base64 inside the JSON: the host serves .json, not .bin.
    var raw = atob(doc.data), buf = new ArrayBuffer(raw.length), b = new Uint8Array(buf);
    for (var i = 0; i < raw.length; i++) { b[i] = raw.charCodeAt(i); }
    var meta = doc.parts;
    layout(meta);
    upload(meta, buf);
    host.classList.add("ready");
    if (status) {
      status.textContent = parts.length + " printed parts, " +
        parts.reduce(function (s, p) { return s + p.tris; }, 0).toLocaleString() +
        " triangles, drawn from the STL files we printed from.";
    }
    show(-1);
    invalidate();
    frame();
  }).catch(function () {
    fail("The 3D model could not be loaded. Every part is in the repository as an STL file.");
  });
})();
