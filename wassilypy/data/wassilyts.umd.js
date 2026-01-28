(function(global, factory) {
  typeof exports === "object" && typeof module !== "undefined" ? factory(exports) : typeof define === "function" && define.amd ? define(["exports"], factory) : (global = typeof globalThis !== "undefined" ? globalThis : global || self, factory(global.wassilyts = {}));
})(this, function(exports2) {
  "use strict";var __defProp = Object.defineProperty;
var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
var __publicField = (obj, key, value) => __defNormalProp(obj, typeof key !== "symbol" ? key + "" : key, value);

  function x(t, r) {
    return t + r;
  }
  function C(t, r) {
    return t - r;
  }
  function s(t) {
    return Array(t).fill(0);
  }
  function p(t, r) {
    let n = s(t.length);
    for (let e = 0; e < t.length; e++)
      n[e] = t[e] + r[e];
    return n;
  }
  function b(t, r) {
    let n = s(t.length);
    for (let e = 0; e < t.length; e++)
      n[e] = Math.min(t[e], r[e]);
    return n;
  }
  function L(t, r) {
    let n = s(t.length);
    for (let e = 0; e < t.length; e++)
      n[e] = Math.max(t[e], r[e]);
    return n;
  }
  function v(t, r) {
    let n = s(r.length);
    for (let e = 0; e < r.length; e++)
      n[e] = t * r[e];
    return n;
  }
  function M(t, r) {
    return p(t, v(-1, r));
  }
  function R(t, r) {
    let n = s(t.length);
    for (let e = 0; e < t.length; e++)
      n[e] = t[e] * r[e];
    return n;
  }
  function Z(t, r) {
    let n = s(t.length);
    for (let e = 0; e < t.length; e++)
      n[e] = t[e] / r[e];
    return n;
  }
  function q(t, r) {
    return t.reduce((n, e, l) => n + e * r[l], 0);
  }
  function g(t) {
    return Math.sqrt(t.reduce((r, n) => r + n * n, 0));
  }
  function B(t) {
    return v(1 / g(t), t);
  }
  function y(t, r = 1e-6) {
    return g(t) < r;
  }
  function D(t, r, n = 1e-6) {
    return y(M(t, r), n);
  }
  function N(t, r) {
    const [n, e, l] = t, [o, f, i] = r;
    return [
      e * i - l * f,
      l * o - n * i,
      n * f - e * o
    ];
  }
  function a(t, r) {
    return Array(t).fill(0).map(() => s(r));
  }
  function P(t, r = [0, 0, 0]) {
    t === null && (t = w(3));
    let n = a(4, 4);
    for (let e = 0; e < 3; e++) {
      for (let l = 0; l < 3; l++)
        n[e][l] = t[e][l];
      n[e][3] = r[e];
    }
    return n[3][3] = 1, n;
  }
  function c(t, r = false) {
    let n = t.length, e = t[0].length;
    if (r) {
      for (let l = 1; l < n; l++)
        if (t[l].length !== e)
          throw new Error(`Row ${l} has ${t[l].length} columns, expected ${e}`);
    }
    return [t.length, t[0].length];
  }
  function S(t) {
    const [r, n] = c(t);
    let e = a(n, r);
    for (let l = 0; l < r; l++)
      for (let o = 0; o < n; o++)
        e[o][l] = t[l][o];
    return e;
  }
  function w(t) {
    let r = a(t, t);
    for (let n = 0; n < t; n++)
      r[n][n] = 1;
    return r;
  }
  function $(t, r) {
    let n = s(t.length);
    for (let e = 0; e < t.length; e++)
      for (let l = 0; l < t[e].length; l++)
        n[e] += t[e][l] * r[l];
    return n;
  }
  function T(t, r) {
    const [n, e] = c(t), [l, o] = c(r);
    if (e !== l)
      throw new Error(`Matrix A has ${e} columns, Matrix B has ${l} rows. Cannot multiply.`);
    let f = a(n, o);
    for (let i = 0; i < n; i++)
      for (let u = 0; u < o; u++)
        for (let h = 0; h < e; h++)
          f[i][u] += t[i][h] * r[h][u];
    return f;
  }
  function d(t) {
    return t.map((r) => r.slice());
  }
  function k(t, r = 1e-3) {
    return t.map((n) => n.map((e) => Math.abs(e - Math.round(e)) < r ? Math.round(e) : e));
  }
  function z(t, r) {
    return $(t, r.concat(1)).slice(0, 3);
  }
  function I(t) {
    return t.reduce((r, n) => r.concat(n), []);
  }
  function F(t, r, n) {
    if (t.length !== r * n)
      throw new Error(`List length ${t.length} does not match ${r}x${n} matrix`);
    let e = a(r, n);
    for (let l = 0; l < r; l++)
      for (let o = 0; o < n; o++)
        e[l][o] = t[l * n + o];
    return e;
  }
  function j(t, r, n, e = false) {
    let l = t;
    e || (l = d(t));
    let o = l[r];
    return l[r] = l[n], l[n] = o, l;
  }
  function m(t, r) {
    const [n, e] = c(t), [l, o] = c(r);
    if (n !== l)
      throw new Error(`Matrix M1 has ${n} rows, Matrix M2 has ${l} rows. Cannot adjoin.`);
    let f = a(n, e + o);
    for (let i = 0; i < n; i++) {
      for (let u = 0; u < e; u++)
        f[i][u] = t[i][u];
      for (let u = 0; u < o; u++)
        f[i][e + u] = r[i][u];
    }
    return f;
  }
  function A(t, r, n, e, l) {
    let o = a(n - r, l - e);
    for (let f = r; f < n; f++)
      for (let i = e; i < l; i++)
        o[f - r][i - e] = t[f][i];
    return o;
  }
  function E(t) {
    let r = d(t), [n, e] = c(r), l = 0;
    for (let o = 0; o < n; o++) {
      if (e <= l)
        return r;
      let f = o;
      for (; r[f][l] === 0; )
        if (f++, n === f && (f = o, l++, e === l))
          return r;
      r = j(r, f, o);
      let i = r[o][l];
      r[o] = r[o].map((u) => u / i);
      for (let u = 0; u < n; u++)
        u !== o && (i = r[u][l], r[u] = M(r[u], v(i, r[o])));
      l++;
    }
    return r;
  }
  function G(t) {
    let [r, n] = c(t);
    if (r !== n)
      throw new Error("Matrix is not square, cannot invert.");
    let e = m(t, w(r));
    return e = E(e), A(e, 0, r, r, 2 * r);
  }
  function H(t) {
    var r = Math.cos(t), n = Math.sin(t), e = [
      [r, -n, 0],
      [n, r, 0],
      [0, 0, 1]
    ];
    return e;
  }
  function J(t) {
    var r = Math.cos(t), n = Math.sin(t), e = [
      [1, 0, 0],
      [0, r, n],
      [0, -n, r]
    ];
    return e;
  }
  function K(t) {
    var r = Math.cos(t), n = Math.sin(t), e = [
      [r, 0, n],
      [0, 1, 0],
      [-n, 0, r]
    ];
    return e;
  }
  const tsVector = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    MAdjoin: m,
    MAsList: I,
    MCopy: d,
    MInverse: G,
    MMProduct: T,
    MRowEchelon: E,
    MTolerate: k,
    MTranspose: S,
    Mpitch: K,
    Mroll: H,
    Mshape: c,
    Mslice: A,
    MswapRows: j,
    MvProduct: $,
    Myaw: J,
    add: x,
    affine3d: P,
    applyAffine3d: z,
    eye: w,
    listAsM: F,
    mZero: a,
    subtract: C,
    vAdd: p,
    vClose: D,
    vCross: N,
    vDiv: Z,
    vDot: q,
    vLength: g,
    vMax: L,
    vMin: b,
    vMul: R,
    vNearlyZero: y,
    vNormalize: B,
    vScale: v,
    vSub: M,
    vZero: s
  }, Symbol.toStringTag, { value: "Module" }));
  var globalCounter = 0;
  class Styled {
    constructor(onFrame = null) {
      __publicField(this, "objectName");
      __publicField(this, "onFrame", null);
      // the frame which contains this object
      __publicField(this, "color", "black");
      __publicField(this, "lineWidth", 1);
      __publicField(this, "lineDash", null);
      __publicField(this, "stroke", false);
      __publicField(this, "textFont", null);
      // font for text, null means use default
      __publicField(this, "lineJoin", null);
      __publicField(this, "defunct", false);
      // true if the object is no longer used
      __publicField(this, "responsive", true);
      // true if the object should respond to events
      __publicField(this, "eventTypeToHandler", /* @__PURE__ */ new Map());
      this.objectName = this.freshName();
      this.onFrame = onFrame;
      if (onFrame) {
        this.styleLike(onFrame);
      }
    }
    /**
     * Create a fresh unique name in this context by appending a global counter to the prefix.
     * @param prefix prefix for new name. If null, use the class name.
     * @returns A fresh unique name string.
     */
    freshName(prefix = null) {
      const base = prefix ? prefix : this.constructor.name;
      const name2 = base + globalCounter;
      globalCounter += 1;
      return name2;
    }
    /** Apply the style of another Styled object to this one.
     * @param other The other Styled object to copy the style from.
     */
    styleLike(other) {
      this.color = other.color;
      this.lineWidth = other.lineWidth;
      if (other.lineDash !== null) {
        this.lineDash = other.lineDash;
      }
      if (other.textFont !== null) {
        this.textFont = other.textFont;
      }
      if (other.lineJoin !== null) {
        this.lineJoin = other.lineJoin;
      }
      this.stroke = other.stroke;
      this.responsive = other.responsive;
    }
    /** Determine if the object is attached to a live frame.
     * @return True if the object is live, false otherwise.
     * @internal
     */
    isLive() {
      if (!this.onFrame) {
        throw new Error("Marking is not attached to a frame.");
      }
      return !this.defunct;
    }
    /** Watch for a specific event type on the containing frame.
     * @param eventType The string name of event to watch for.
     * @internal
     */
    watchEvent(eventType) {
      if (!this.onFrame) {
        throw new Error("Marking is not attached to a frame.");
      }
      this.onFrame.watchEvent(eventType);
    }
    /** Request a redraw of the frame containing this object. */
    requestRedraw() {
      if (!this.isLive()) {
        return;
      }
      this.onFrame.requestRedraw();
    }
    /** Rename this element in the containing frame,
     * @param newname The new name for this object.
     */
    rename(newname) {
      if (!this.onFrame) {
        this.objectName = newname;
        return;
      }
      this.onFrame.renameElement(this, newname);
    }
    /**
     * Determine if the object is picked by a mouse event.
     * @param canvasXY the canvas coordinates of the mouse event.
     * @returns True if the object is picked, false otherwise.
     */
    pickObject(canvasXY) {
      return this.responsive && !this.defunct;
    }
    /** Default mouse event handler.
     * @internal
     * @param eventType The type of mouse event.
     * @param canvasXY The canvas coordinates of the mouse event.
     * @param cartesianXY The cartesian pixel coordinates of the mouse event.
     * @param frameXY The frame model coordinates of the mouse event.
     * @returns True if the event was handled, false otherwise.
     */
    mouseEventHandler(eventType, canvasXY, cartesianXY, frameXY) {
      if (!this.responsive) {
        return false;
      }
      const handler = this.eventTypeToHandler.get(eventType);
      if (handler) {
        if (!this.defunct && this.pickObject(canvasXY)) {
          return handler(this, eventType, canvasXY, cartesianXY, frameXY);
        }
      }
      return false;
    }
    /** Set an event handler for a specific event type
     * @param eventType The string name of the event.
     * @param handler The event handler function or null to remove.
     * @returns The styled object for chaining.
     */
    onEvent(eventType, handler) {
      this.watchEvent(eventType);
      if (handler === null) {
        this.eventTypeToHandler.delete(eventType);
      } else {
        this.eventTypeToHandler.set(eventType, handler);
      }
      return this;
    }
    /** Set a "final" event handler which always returns true and does not recieve the this object (for external serialization))
     * @param eventType The string name of the event.
     * @param handler The external event handler function or null to remove.
     * @returns The styled object for chaining.
     */
    handleEvent(eventType, handler) {
      if (handler === null) {
        this.eventTypeToHandler.delete(eventType);
      } else {
        const internalHandler = (element, eventType2, canvasXY, cartesianXY, frameXY) => {
          let name2 = null;
          if (element !== null) {
            name2 = element.objectName;
          }
          handler(name2, eventType2, canvasXY, cartesianXY, frameXY);
          return true;
        };
        this.onEvent(eventType, internalHandler);
      }
      return this;
    }
    /** Prepare the object for redraw.
     * @internal
     */
    prepareForRedraw() {
    }
    join(join) {
      this.lineJoin = join;
      this.requestRedraw();
      return this;
    }
    /** Set the font for text, null means use default.
     * @param font The font string to set.
     * @returns The styled object for chaining.
     */
    font(font) {
      this.textFont = font;
      this.requestRedraw();
      return this;
    }
    /** Set the object to be stroked when drawn.
     * @returns The styled object for chaining.
     */
    stroked() {
      this.stroke = true;
      this.requestRedraw();
      return this;
    }
    /** Set the object to be filled when drawn.
     * @returns The styled object for chaining.
     */
    filled() {
      this.stroke = false;
      this.requestRedraw();
      return this;
    }
    /** Set the color for the object.
     * @param color The color string to set.
     * @returns The styled object for chaining.
     */
    colored(color) {
      this.color = color;
      this.requestRedraw();
      return this;
    }
    /** Set the line width for the object.
     * @param width The line width to set.
     * @returns The styled object for chaining.
     */
    linedWidth(width) {
      this.lineWidth = width;
      this.requestRedraw();
      return this;
    }
    /** Set the line dash pattern for the object.
     * @param dash The line dash pattern to set, or null for solid line.
     * @returns The styled object for chaining.
     */
    dashed(dash) {
      this.lineDash = dash;
      this.requestRedraw();
      return this;
    }
    /** Apply the style to a canvas rendering context.
     * @internal
     * @param ctx The canvas rendering context to apply the style to.
     */
    applyStyle(ctx) {
      ctx.strokeStyle = this.color;
      ctx.fillStyle = this.color;
      if (this.lineWidth) {
        ctx.lineWidth = this.lineWidth;
      }
      if (this.lineDash) {
        ctx.setLineDash(this.lineDash);
      }
      if (this.textFont) {
        ctx.font = this.textFont;
      }
      if (this.lineJoin) {
        ctx.lineJoin = this.lineJoin;
      }
    }
    /** Forget this object from the containing frame and diagram. */
    forget() {
      this.defunct = true;
      this.requestRedraw();
    }
  }
  const styled = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    Styled
  }, Symbol.toStringTag, { value: "Module" }));
  class Marking extends Styled {
    constructor() {
      super(...arguments);
      __publicField(this, "stroke", false);
    }
    // default draw method
    draw() {
      if (!this.isLive()) {
        return;
      }
      const path = this.drawPath();
      this.prepare();
      const ctx = this.onFrame.diagram.ctx;
      if (this.stroke) {
        ctx.stroke(path);
      } else {
        ctx.fill(path);
      }
      ctx.restore();
    }
    pickObject(canvasXY) {
      if (!this.isLive()) {
        return false;
      }
      const path = this.drawPath();
      const ctx = this.onFrame.diagram.ctx;
      const result = ctx.isPointInPath(path, canvasXY[0], canvasXY[1]);
      return result;
    }
    // prepare the context for drawing, return false if no change.
    // save state if changed.
    prepare() {
      if (!this.isLive()) {
        return false;
      }
      const ctx = this.onFrame.diagram.ctx;
      ctx.save();
      this.applyStyle(ctx);
      return true;
    }
    /** Get the reference point of the marking in cartesian pixel coordinates. */
    getPixel() {
      if (!this.isLive()) {
        throw new Error("Marking is not attached to a frame.");
      }
      return this.onFrame.toPixel(this.getFramePoint());
    }
    /** Set the reference point of the marking in cartesian pixel coordinates. */
    setPixel(position) {
      if (!this.isLive()) {
        throw new Error("Marking is not attached to a frame.");
      }
      this.setFramePoint(this.onFrame.toModel(position));
      this.requestRedraw();
    }
  }
  const marking = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    Marking
  }, Symbol.toStringTag, { value: "Module" }));
  class Circle extends Marking {
    constructor(frame2, center, radius, scaled = true) {
      super(frame2);
      __publicField(this, "center");
      __publicField(this, "radius");
      __publicField(this, "scaled");
      this.center = center;
      this.radius = radius;
      this.scaled = scaled;
    }
    centerAt(position) {
      this.center = position;
      this.requestRedraw();
      return this;
    }
    resize(radius) {
      this.radius = radius;
      this.requestRedraw();
      return this;
    }
    scaling(scaled) {
      this.scaled = scaled;
      this.requestRedraw();
      return this;
    }
    setFramePoint(position) {
      this.center = position;
    }
    getFramePoint() {
      return this.center;
    }
    drawPath() {
      if (!this.isLive()) {
        throw new Error("Circle is not attached to a frame.");
      }
      const frame2 = this.onFrame;
      const path = new Path2D();
      const center = this.center;
      let radius = this.radius;
      const pixelCenter = frame2.addPoint(center);
      const ccenter = frame2.diagram.toCartesian(pixelCenter);
      if (this.scaled) {
        const offset = [center[0] + radius, center[1]];
        const pixelOffset = frame2.addPoint(offset);
        const pixelRadius = g(M(pixelCenter, pixelOffset));
        radius = pixelRadius;
      }
      const [px, py] = pixelCenter;
      path.arc(px, py, radius, 0, 2 * Math.PI);
      frame2.addPixelPoint(p(ccenter, [radius, 0]));
      frame2.addPixelPoint(p(ccenter, [0, radius]));
      frame2.addPixelPoint(p(ccenter, [-radius, 0]));
      frame2.addPixelPoint(p(ccenter, [0, -radius]));
      return path;
    }
  }
  const circle = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    Circle
  }, Symbol.toStringTag, { value: "Module" }));
  function rgb(direction, alpha = null, epsilon = 1e-6) {
    if (direction.length !== 3) {
      throw new Error("Direction must be a 3D vector.");
    }
    const len = g(direction);
    let shifted = [0.5, 0.5, 0.5];
    if (len > epsilon) {
      let halve = 0.5 / len;
      let halved = v(halve, direction);
      shifted = p(halved, [0.5, 0.5, 0.5]);
    }
    const [r, g$1, b2] = shifted.map((x2) => Math.round(x2 * 255));
    if (alpha !== null) {
      return `rgba(${r}, ${g$1}, ${b2}, ${alpha})`;
    } else {
      return `rgb(${r}, ${g$1}, ${b2})`;
    }
  }
  function panel(container, minxy, maxxy, width, height = null, epsilon = 1e-6) {
    let element;
    if (typeof container === "string") {
      const el = document.getElementById(container);
      if (el === null) {
        throw new Error(`Container element with id ${container} not found.`);
      }
      element = el;
    } else {
      element = container;
    }
    const extent = M(maxxy, minxy);
    if (Math.min(...extent) < epsilon) {
      throw new Error("The extent of the coordinates is too small to create a frame.");
    }
    if (width <= 0) {
      throw new Error("Width must be greater than zero.");
    }
    if (height === null) {
      const aspect = extent[1] / extent[0];
      height = width * aspect;
    }
    if (height <= 0) {
      throw new Error("Height must be greater than zero.");
    }
    const mainFrame = drawOn(element, width, height);
    const fromMin = [0, 0];
    const fromMax = [width, height];
    const scaledFrame = mainFrame.regionFrame(
      fromMin,
      fromMax,
      minxy,
      maxxy
    );
    return scaledFrame;
  }
  function swatch(container, pixelWidth, modelWidth, modelCenter = null, epsilon = 1e-6) {
    if (modelCenter === null) {
      modelCenter = [0, 0];
    }
    const width2 = modelWidth / 2;
    const offset = [width2, width2];
    const minxy = M(modelCenter, offset);
    const maxxy = p(modelCenter, offset);
    const result = panel(
      container,
      minxy,
      maxxy,
      pixelWidth,
      pixelWidth,
      epsilon
    );
    return result;
  }
  function cube(container, pixelWidth, modelWidth, modelCenter = null, perspective = true, shrinkFactor = 0.9, epsilon = 1e-6) {
    if (modelCenter === null) {
      modelCenter = [0, 0, 0];
    }
    const eye_offset = [0, 0, -1.5 * modelWidth];
    const eye = p(modelCenter, eye_offset);
    const lookAt = modelCenter;
    const up = [0, 1, 0];
    const swatchWidth = modelWidth * shrinkFactor;
    const onPanel = swatch(
      container,
      pixelWidth,
      swatchWidth,
      [modelCenter[0], modelCenter[1]],
      epsilon
    );
    const cubeFrame = onPanel.frame3d(
      eye,
      lookAt,
      perspective,
      up
    );
    return cubeFrame;
  }
  class Rotation2d {
    constructor(degrees, about = [0, 0]) {
      __publicField(this, "degrees");
      __publicField(this, "about");
      __publicField(this, "matrix");
      this.degrees = degrees;
      this.about = about;
      const tx = this.about[0];
      const ty = this.about[1];
      const radians = degrees * Math.PI / 180;
      const cosTheta = Math.cos(radians);
      const sinTheta = Math.sin(radians);
      const affineShiftMatrix = [
        [1, 0, -tx],
        [0, 1, -ty],
        [0, 0, 1]
      ];
      const rotationMatrix = [
        [cosTheta, -sinTheta, 0],
        [sinTheta, cosTheta, 0],
        [0, 0, 1]
      ];
      const affineUnshiftMatrix = [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
      ];
      let tempMatrix = T(rotationMatrix, affineShiftMatrix);
      this.matrix = T(affineUnshiftMatrix, tempMatrix);
    }
    transformPoint(xy) {
      if (xy.length !== 2) {
        throw new Error("Point must be a 2D vector.");
      }
      const pointHomogeneous = [xy[0], xy[1], 1];
      const transformedHomogeneous = $(this.matrix, pointHomogeneous);
      return [transformedHomogeneous[0], transformedHomogeneous[1]];
    }
    applyToCanvas(ctx) {
      const m2 = this.matrix;
      const [a2, c2, e] = m2[0];
      const [b2, d2, f] = m2[1];
      ctx.transform(
        a2,
        b2,
        c2,
        d2,
        e,
        f
      );
    }
  }
  const conveniences = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    Rotation2d,
    cube,
    panel,
    rgb,
    swatch
  }, Symbol.toStringTag, { value: "Module" }));
  class Rectangle extends Marking {
    constructor(frame2, point, size = null, offset = [0, 0], scaled = true, rotationDegrees = 0) {
      super(frame2);
      __publicField(this, "point");
      __publicField(this, "size");
      __publicField(this, "offset");
      __publicField(this, "scaled");
      __publicField(this, "rotationDegrees", 0);
      this.point = point;
      this.size = size;
      this.offset = offset;
      this.scaled = scaled;
      this.rotationDegrees = rotationDegrees;
    }
    degrees(rotationDegrees) {
      this.rotationDegrees = rotationDegrees;
      this.requestRedraw();
      return this;
    }
    resize(size) {
      this.size = size;
      this.requestRedraw();
      return this;
    }
    offsetBy(offset) {
      this.offset = offset;
      this.requestRedraw();
      return this;
    }
    setScaled(scaled) {
      this.scaled = scaled;
      this.requestRedraw();
      return this;
    }
    locateAt(position) {
      this.point = position;
      this.requestRedraw();
      return this;
    }
    setFramePoint(position) {
      this.point = position;
    }
    getFramePoint() {
      return this.point;
    }
    /* unrotated rectangle path
    drawPath(): Path2D {
        if (!this.isLive()) {
            throw new Error("Rectangle is not attached to a frame.");
        }
        const frame = this.onFrame!;
        const path = new Path2D();
        let pixelStart: tsvector.Vector;
        let pixelSize: tsvector.Vector;
        ({pixelStart, pixelSize} = this.getPixelStartAndSize());
        //const [px, py] = pixelStart;
        const [sx, sy] = pixelSize;
        //const cstart = frame.diagram.toCartesian(pixelStart);
        const [cx, cy] = frame.diagram.toCanvas(pixelStart);
        path.rect(cx, cy, sx, -sy);
        //console.log(`translated rectangle at ${this.point} with size ${this.size}`);
        //console.log(`to rectangle at ${cx}, ${cy} with size ${this.size}`);
        //console.log("sx, sy: ", sx, sy);
        // add reference points to diagram
        frame.addPixelPoint(pixelStart);
        frame.addPixelPoint(tsvector.vAdd(pixelStart, [sx, 0]));
        frame.addPixelPoint(tsvector.vAdd(pixelStart, [0, sy]));
        frame.addPixelPoint(tsvector.vAdd(pixelStart, pixelSize));
        return path;
    };
    */
    // rotated rectangle path
    drawPath() {
      if (!this.isLive()) {
        throw new Error("Rectangle is not attached to a frame.");
      }
      const frame2 = this.onFrame;
      const path = new Path2D();
      let pixelStart;
      let pixelSize;
      ({ pixelStart, pixelSize } = this.getPixelStartAndSize());
      const pixelPoint = frame2.toPixel(this.point);
      const canvasPoint = frame2.diagram.toCanvas(pixelPoint);
      const [sx, sy] = pixelSize;
      const rotation = new Rotation2d(-this.rotationDegrees, canvasPoint);
      const canvasStart = frame2.diagram.toCanvas(pixelStart);
      const unrotatedCorners = [
        canvasStart,
        p(canvasStart, [sx, 0]),
        p(canvasStart, [sx, -sy]),
        p(canvasStart, [0, -sy])
      ];
      const rotatedCorners = unrotatedCorners.map((pix) => {
        return rotation.transformPoint(pix);
      });
      const [fx, fy] = rotatedCorners[0];
      path.moveTo(fx, fy);
      rotatedCorners.slice(1).forEach((corner) => {
        const [x2, y2] = corner;
        path.lineTo(x2, y2);
      });
      path.closePath();
      rotatedCorners.forEach((corner) => {
        frame2.addPixelPoint(frame2.diagram.toCartesian(corner));
      });
      return path;
    }
    getPixelStartAndSize() {
      let size = this.size;
      if (size === null) {
        throw new Error("Rectangle size is not defined.");
      }
      if (!this.isLive()) {
        throw new Error("Rectangle is not attached to a frame.");
      }
      const frame2 = this.onFrame;
      let pixelStart;
      let pixelSize;
      let point = this.point;
      let offset = this.offset;
      let lowerLeftCartesian;
      let upperLeftCartesian;
      if (this.scaled) {
        let lowerleftFrame = p(point, offset);
        let upperleftFrame = p(lowerleftFrame, size);
        lowerLeftCartesian = frame2.toPixel(lowerleftFrame);
        upperLeftCartesian = frame2.toPixel(upperleftFrame);
      } else {
        let pointCartesian = frame2.toPixel(point);
        lowerLeftCartesian = p(pointCartesian, offset);
        upperLeftCartesian = p(lowerLeftCartesian, size);
      }
      let [llx, lly] = lowerLeftCartesian;
      let [ulx, uly] = upperLeftCartesian;
      pixelStart = [Math.min(llx, ulx), Math.min(lly, uly)];
      let pixelEnd = [Math.max(llx, ulx), Math.max(lly, uly)];
      pixelSize = M(pixelEnd, pixelStart);
      return { pixelStart, pixelSize };
    }
    getPixelStartAndSize0() {
      let size = this.size;
      if (size === null) {
        throw new Error("Rectangle size is not defined.");
      }
      if (!this.isLive()) {
        throw new Error("Rectangle is not attached to a frame.");
      }
      const frame2 = this.onFrame;
      let pixelStart;
      let pixelSize;
      if (this.scaled) {
        const start = p(this.point, this.offset);
        const end = p(start, size);
        pixelStart = frame2.toPixel(start);
        const endPixel = frame2.toPixel(end);
        pixelSize = M(endPixel, pixelStart);
      } else {
        const offset1 = [this.offset[0], -this.offset[1]];
        const size1 = [size[0], -size[1]];
        const pointPixel = frame2.toPixel(this.point);
        pixelStart = p(pointPixel, offset1);
        pixelSize = size1;
      }
      return { pixelStart, pixelSize };
    }
  }
  function Square(frame2, point, size, offset = null, scaled = false) {
    if (offset === null) {
      const half = size / 2;
      offset = [-half, -half];
    }
    return new Rectangle(frame2, point, [size, size], offset, scaled);
  }
  const rect = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    Rectangle,
    Square
  }, Symbol.toStringTag, { value: "Module" }));
  class Line extends Marking {
    constructor(frame2, start, end) {
      super(frame2);
      __publicField(this, "start");
      __publicField(this, "end");
      this.start = start;
      this.end = end;
      this.stroked();
    }
    startAt(position) {
      this.start = position;
      this.requestRedraw();
      return this;
    }
    endAt(position) {
      this.end = position;
      this.requestRedraw();
      return this;
    }
    getFramePoint() {
      return this.start;
    }
    setFramePoint(position) {
      const offset = M(position, this.start);
      this.start = position;
      this.end = p(this.end, offset);
    }
    drawPath() {
      if (!this.isLive()) {
        throw new Error("Line is not attached to a frame.");
      }
      const frame2 = this.onFrame;
      const path = new Path2D();
      let pixelStart = frame2.addPoint(this.start);
      let pixelEnd = frame2.addPoint(this.end);
      const [sx, sy] = pixelStart;
      const [ex, ey] = pixelEnd;
      path.moveTo(sx, sy);
      path.lineTo(ex, ey);
      return path;
    }
  }
  const line = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    Line
  }, Symbol.toStringTag, { value: "Module" }));
  class Poly extends Marking {
    constructor(frame2, points) {
      super(frame2);
      __publicField(this, "points");
      __publicField(this, "close", true);
      this.points = points;
      this.stroked();
    }
    vertices(points) {
      this.points = points;
      this.requestRedraw();
      return this;
    }
    closed(value = true) {
      this.close = value;
      this.requestRedraw();
      return this;
    }
    getFramePoint() {
      return this.points[0];
    }
    setFramePoint(position) {
      const offset = M(position, this.points[0]);
      this.points = this.points.map((point) => p(point, offset));
    }
    drawPath() {
      if (!this.isLive()) {
        throw new Error("Polygon is not attached to a frame.");
      }
      const frame2 = this.onFrame;
      const path = new Path2D();
      const pixelPoints = this.points.map((xy) => frame2.addPoint(xy));
      const [sx, sy] = pixelPoints[0];
      path.moveTo(sx, sy);
      pixelPoints.slice(1).forEach((xy) => {
        const [x2, y2] = xy;
        path.lineTo(x2, y2);
      });
      if (this.close) {
        path.closePath();
      }
      pixelPoints.forEach((xy) => {
        frame2.addPixelPoint(frame2.diagram.toCartesian(xy));
      });
      return path;
    }
  }
  const poly = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    Poly
  }, Symbol.toStringTag, { value: "Module" }));
  class Orbiter {
    constructor(frame3d2) {
      __publicField(this, "frame3d");
      __publicField(this, "projection");
      __publicField(this, "startXY", null);
      __publicField(this, "endXY", null);
      //originalMatrix: tsvector.Matrix | null = null;
      __publicField(this, "originalProjector");
      this.frame3d = frame3d2;
      this.projection = frame3d2.projection;
      this.originalProjector = frame3d2.projection;
      const onFrame = frame3d2.onFrame;
      onFrame.onEvent("pointerdown", (element, eventType, canvasXY, cartesianXY, frameXY) => {
        return this.pointerDownHandler(element, eventType, canvasXY, cartesianXY, frameXY);
      });
      onFrame.onEvent("pointermove", (element, eventType, canvasXY, cartesianXY, frameXY) => {
        return this.pointerMoveHandler(element, eventType, canvasXY, cartesianXY, frameXY);
      });
      onFrame.onEvent("pointerup", (element, eventType, canvasXY, cartesianXY, frameXY) => {
        return this.pointerUpHandler(element, eventType, canvasXY, cartesianXY, frameXY);
      });
      onFrame.onEvent("pointerout", (element, eventType, canvasXY, cartesianXY, frameXY) => {
        return this.pointerUpHandler(element, eventType, canvasXY, cartesianXY, frameXY);
      });
      onFrame.responsive = true;
    }
    doRotation(endXY) {
      if (this.startXY === null) {
        throw new Error("startXY is null, cannot perform rotation.");
      }
      this.endXY = endXY;
      const projection2 = this.projection;
      const rotation = projection2.XYOffsetRotation(
        this.startXY,
        this.endXY
      );
      const newProjection = projection2.rotation(rotation);
      this.frame3d.projection = newProjection;
      this.frame3d.requestRedraw();
    }
    pointerDownHandler(element, eventType, canvasXY, cartesianXY, frameXY) {
      this.startXY = frameXY;
      this.projection = this.frame3d.projection;
      return true;
    }
    pointerMoveHandler(element, eventType, canvasXY, cartesianXY, frameXY) {
      if (this.startXY === null) {
        return false;
      }
      this.endXY = frameXY;
      this.doRotation(this.endXY);
      return true;
    }
    pointerUpHandler(element, eventType, canvasXY, cartesianXY, frameXY) {
      this.pointerMoveHandler(element, eventType, canvasXY, cartesianXY, frameXY);
      this.startXY = null;
      this.endXY = null;
      return true;
    }
  }
  class Marking3d extends Styled {
    // depth can be calculated or set
    constructor(onFrame3d) {
      super(onFrame3d.onFrame);
      __publicField(this, "onFrame3d");
      __publicField(this, "depthValue", null);
      this.onFrame3d = onFrame3d;
      this.styleLike(onFrame3d);
    }
    depth() {
      if (this.depthValue !== null) {
        return this.depthValue;
      } else {
        throw new Error("Depth not set for Marking3d.");
      }
    }
    to2d(from3dProjected) {
      return [from3dProjected[0], from3dProjected[1]];
    }
    // trivial getPixel, setPixel, and draw methods
    getPixel() {
      return [];
    }
    setPixel(position) {
    }
    draw() {
    }
    forget() {
      this.onFrame3d.nameToMarking3d.delete(this.objectName);
      this.onFrame3d.onFrame.diagram.nameToStyled.delete(this.objectName);
      this.defunct = true;
      this.requestRedraw();
    }
  }
  const marking3d = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    Marking3d
  }, Symbol.toStringTag, { value: "Module" }));
  class Line3d extends Marking3d {
    constructor(start, end, onFrame3d) {
      super(onFrame3d);
      __publicField(this, "start");
      __publicField(this, "end");
      this.start = start;
      this.end = end;
      this.stroked();
    }
    projectTo2D() {
      const onFrame3d = this.onFrame3d;
      const startProj = onFrame3d.projection.project(this.start);
      const endProj = onFrame3d.projection.project(this.end);
      this.depthValue = (startProj[2] + endProj[2]) / 2;
      const result = this.onFrame.line(this.to2d(startProj), this.to2d(endProj));
      result.styleLike(this);
      return result;
    }
  }
  const line3d = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    Line3d
  }, Symbol.toStringTag, { value: "Module" }));
  class Poly3d extends Marking3d {
    constructor(points, onFrame3d) {
      super(onFrame3d);
      __publicField(this, "points");
      __publicField(this, "close", true);
      this.points = points;
    }
    closed(value = true) {
      this.close = value;
      this.requestRedraw();
      return this;
    }
    projectTo2D() {
      const projectedPoints = this.points.map((point) => this.onFrame3d.projection.project(point));
      const points2d = projectedPoints.map((p2) => this.to2d(p2));
      const poly2d = this.onFrame.polygon(points2d);
      poly2d.closed(this.close);
      poly2d.styleLike(this);
      this.depthValue = projectedPoints.reduce((sum, p2) => sum + p2[2], 0) / projectedPoints.length;
      return poly2d;
    }
  }
  const poly3d = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    Poly3d
  }, Symbol.toStringTag, { value: "Module" }));
  class Circle3d extends Marking3d {
    constructor(center, radius, onFrame3d, scaled = true) {
      super(onFrame3d);
      __publicField(this, "center");
      __publicField(this, "radius");
      __publicField(this, "scaled");
      this.center = center;
      this.radius = radius;
      this.scaled = scaled;
    }
    projectTo2D() {
      const centerProj = this.onFrame3d.projection.project(this.center);
      const center2d = this.to2d(centerProj);
      this.depthValue = centerProj[2];
      let radius = this.radius;
      if (this.scaled) {
        const scale = this.onFrame3d.projection.distanceScale(this.center);
        radius = this.radius * scale;
      }
      const circle2d = this.onFrame.circle(center2d, radius, this.scaled);
      circle2d.styleLike(this);
      return circle2d;
    }
  }
  class Rect3d extends Marking3d {
    constructor(point, size = null, offset = [0, 0], onFrame3d, scaled = true, rotationDegrees = 0) {
      super(onFrame3d);
      __publicField(this, "point");
      __publicField(this, "size");
      __publicField(this, "offset");
      __publicField(this, "scaled");
      __publicField(this, "rotationDegrees", 0);
      this.point = point;
      this.size = size;
      this.offset = offset;
      this.scaled = scaled;
      this.rotationDegrees = rotationDegrees;
    }
    projectTo2D() {
      const { point2d, size, offset } = this.geometry2d();
      const rect2d = this.onFrame.rect(point2d, size, offset, this.scaled, this.rotationDegrees);
      rect2d.styleLike(this);
      return rect2d;
    }
    geometry2d() {
      if (this.scaled && this.size === null) {
        throw new Error("Rect3d size is null, cannot project to 2D.");
      }
      const pointProj = this.onFrame3d.projection.project(this.point);
      const point2d = this.to2d(pointProj);
      this.depthValue = pointProj[2];
      let size = this.size;
      let offset = this.offset;
      if (this.scaled) {
        const scale = this.onFrame3d.projection.distanceScale(this.point);
        size = v(scale, size);
        offset = v(scale, offset);
      }
      return { point2d, size, offset };
    }
    // xxx this should use mixin like tricks...
    degrees(rotationDegrees) {
      this.rotationDegrees = rotationDegrees;
      this.requestRedraw();
      return this;
    }
    resize(size) {
      this.size = size;
      this.requestRedraw();
      return this;
    }
    offsetBy(offset) {
      this.offset = offset;
      this.requestRedraw();
      return this;
    }
    setScaled(scaled) {
      this.scaled = scaled;
      this.requestRedraw();
      return this;
    }
    locateAt(position) {
      this.point = position;
      this.requestRedraw();
      return this;
    }
    setFramePoint(position) {
      this.point = position;
    }
  }
  class Image3d extends Rect3d {
    constructor(name2, point, size = null, offset = [0, 0], onFrame3d, scaled = false, rotationDegrees = 0) {
      super(point, size, offset, onFrame3d, scaled, rotationDegrees);
      __publicField(this, "imagename");
      this.imagename = name2;
    }
    projectTo2D() {
      const { point2d, size, offset } = this.geometry2d();
      const image2d = this.onFrame.namedImage(point2d, this.imagename, size, offset, this.scaled);
      image2d.degrees(this.rotationDegrees);
      image2d.styleLike(this);
      return image2d;
    }
  }
  class TextBox3d extends Rect3d {
    constructor(text, point, shift = [0, 0], alignment = "left", background = null, onFrame3d) {
      const dummyoffset = [0, 0];
      super(point, null, dummyoffset, onFrame3d, false, 0);
      __publicField(this, "text");
      __publicField(this, "alignment");
      __publicField(this, "background");
      __publicField(this, "shift");
      this.text = text;
      this.alignment = alignment;
      this.background = background;
      this.shift = shift;
    }
    projectTo2D() {
      const { point2d, size, offset } = this.geometry2d();
      const textbox2d = this.onFrame.textBox(
        point2d,
        this.text,
        offset,
        this.alignment,
        this.background
      );
      textbox2d.degrees(this.rotationDegrees);
      textbox2d.styleLike(this);
      return textbox2d;
    }
  }
  class Frame3d extends Styled {
    constructor(fromFrame, projection2) {
      super(fromFrame);
      __publicField(this, "projection");
      //fromFrame: frame.Frame;
      __publicField(this, "onFrame");
      __publicField(this, "nameToMarking3d", /* @__PURE__ */ new Map());
      __publicField(this, "orbiter", null);
      this.projection = projection2;
      this.onFrame = new Frame(fromFrame.diagram, null, fromFrame);
      fromFrame.addElement(this.onFrame);
    }
    requestRedraw() {
      this.onFrame.requestRedraw();
    }
    /**
     * Set up an orbiter to control this frame to allow interactive rotation via mouse dragging.
     * @returns orbiter.Orbiter
     */
    orbit() {
      if (this.orbiter === null) {
        this.orbiter = new Orbiter(this);
      }
      return this.orbiter;
    }
    /**
     * Clear all 3D markings from this frame.
     */
    clear() {
      this.nameToMarking3d.forEach((element) => {
        element.forget();
      });
      this.nameToMarking3d.clear();
      this.onFrame.clear();
    }
    /**
     * Prepare the 3D frame for redraw by projecting all 3D markings to 2D and drawing them in depth order.
     * @internal
     */
    prepareForRedraw() {
      this.onFrame.clear();
      this.onFrame.styleLike(this);
      const depthsAndMarkings = [];
      this.nameToMarking3d.forEach((marking3d2) => {
        const marking2d = marking3d2.projectTo2D();
        const depth = marking3d2.depth();
        depthsAndMarkings.push([depth, marking2d]);
      });
      depthsAndMarkings.sort((a2, b2) => b2[0] - a2[0]);
      depthsAndMarkings.forEach(([, marking2d]) => {
        this.onFrame.addElement(marking2d);
      });
      this.onFrame.prepareForRedraw();
    }
    /**
     * Fit the frame to enclose all 3D markings.
     * @param border Number of pixels of border to leave around the fitted markings.
     */
    fit(border = 0) {
      if (this.nameToMarking3d.size === 0) {
        return;
      }
      this.onFrame.fit(border);
    }
    /**
     * Draw the frame by drawing the onFrame.
     * @internal
     */
    draw() {
      this.onFrame.draw();
    }
    /**
     * Return the pixel position of the frame in the diagram.
     * @returns [number, number] pixel position
     */
    getPixel() {
      return this.onFrame.getPixel();
    }
    /**
     * set the pixel position of the frame in the diagram.  
     * @param position 
     */
    setPixel(position) {
      this.onFrame.setPixel(position);
    }
    /**
     * Register an image with a name in the frame's image cache.
     * @param name 
     * @param image 
     * @returns frame3d.Frame3d for chaining
     */
    nameImage(name2, image) {
      this.onFrame.nameImage(name2, image);
      return this;
    }
    /**
     * Register an image from a URL with a name in the frame's image cache.
     * @param name 
     * @param url 
     * @returns frame3d.Frame3d for chaining
     */
    nameImageFromURL(name2, url) {
      this.onFrame.nameImageFromURL(name2, url);
      return this;
    }
    /**
     * Position a named image in 3D space.
     * @param point 
     * @param imagename 
     * @param size 
     * @param offset 
     * @param scaled 
     * @returns 
     */
    namedImage(point, imagename, size = null, offset = [0, 0], scaled = false) {
      const image = new Image3d(imagename, point, size, offset, this, scaled);
      this.nameToMarking3d.set(image.objectName, image);
      return image;
    }
    /**
     * Position a text box in 3D space.
     * @param point the position of the text box in 3D space
     * @param text the text string
     * @param shift 
     * @param alignment the text alignment like "left", "center, "right"
     * @param background background color string or null for no background
     * @returns text3d.TextBox3d
     */
    textBox(point, text, shift = [0, 0], alignment = "left", background = null) {
      const textbox = new TextBox3d(text, point, shift, alignment, background, this);
      this.nameToMarking3d.set(textbox.objectName, textbox);
      return textbox;
    }
    /**
     * Position a 3D line marking between two points.
     * @param start 
     * @param end 
     * @returns line3d.Line3d
     */
    line(start, end) {
      const line2 = new Line3d(start, end, this);
      this.nameToMarking3d.set(line2.objectName, line2);
      return line2;
    }
    /**
     * Add a polygon of polyline marking in 3D space.
     * Use poly.closed(false) to make it a polyline.
     * Use poly.stroked(), .filled(), .colored(), etc to style it.
     * @param points 
     * @returns 
     */
    poly(points) {
      const poly2 = new Poly3d(points, this);
      this.nameToMarking3d.set(poly2.objectName, poly2);
      return poly2;
    }
    /**
     * Add a circle marking in 3D space.
     * @param center the center of the circle in 3D space
     * @param radius the radius of the circle
     * @returns circle3d.Circle3d
     */
    circle(center, radius) {
      const circle2 = new Circle3d(center, radius, this);
      this.nameToMarking3d.set(circle2.objectName, circle2);
      return circle2;
    }
    /**
     * Add a rectangle marking in 3D space.
     * @param point the position of the rectangle in 3D space
     * @param size the size of the rectangle in 3D space
     * @param offset the offset of the rectangle in 3D space
     * @param scaled whether to scale the rectangle
     * @param rotationDegrees the rotation of the rectangle in degrees
     * @returns rect3d.Rect3d
     */
    rect(point, size, offset = [0, 0], scaled = true, rotationDegrees = 0) {
      const rectangle = new Rect3d(point, size, offset, this, scaled, rotationDegrees);
      this.nameToMarking3d.set(rectangle.objectName, rectangle);
      return rectangle;
    }
  }
  const frame3d = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    Frame3d
  }, Symbol.toStringTag, { value: "Module" }));
  const EPSILON = 1e-6;
  function perpendicularComponent(toVector, fromVector) {
    const V = toVector;
    const D2 = fromVector;
    const n = B(V);
    const dot = q(n, D2);
    const proj = v(dot, n);
    const perp = M(D2, proj);
    return perp;
  }
  function affine3d(xyz) {
    return [xyz[0], xyz[1], xyz[2], 1];
  }
  function ProjectionMatrix(eyePoint, lookAtPoint, upVector = null, epsilon = EPSILON) {
    const E2 = eyePoint;
    const C2 = lookAtPoint;
    const direction = M(C2, E2);
    const length = g(direction);
    if (length < epsilon) {
      throw new Error("Eye point and look at point are too close together.");
    }
    const Vz = B(direction);
    if (upVector === null) {
      upVector = [0, 1, 0];
    }
    upVector = perpendicularComponent(Vz, upVector);
    if (g(upVector) < epsilon) {
      upVector = perpendicularComponent(Vz, [1, 1, 0]);
    }
    const up = B(upVector);
    const right = B(N(up, Vz));
    const At = [
      affine3d(p(E2, right)),
      affine3d(p(E2, up)),
      affine3d(p(E2, Vz)),
      // don't distort the Z axis
      affine3d(E2)
    ];
    const A2 = S(At);
    const B$1 = [
      [1, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 1, 0],
      [1, 1, 1, 1]
    ];
    const invA = G(A2);
    const result = T(B$1, invA);
    return result;
  }
  class Projector {
    constructor(eyePoint, lookAtPoint, perspective = true, upVector = null) {
      __publicField(this, "eyePoint");
      __publicField(this, "lookAtPoint");
      __publicField(this, "upVector");
      __publicField(this, "projectionMatrix", null);
      __publicField(this, "focusLength", 1);
      // distance from eye to focus point
      __publicField(this, "zscale", 1);
      __publicField(this, "perspective", true);
      this.eyePoint = eyePoint;
      this.lookAtPoint = lookAtPoint;
      if (upVector === null) {
        upVector = [0, 1, 0];
      }
      this.upVector = upVector;
      this.perspective = perspective;
      this.getProjectionMatrix();
    }
    lookAt(lookAtPoint, epsilon = EPSILON) {
      this.lookAtPoint = lookAtPoint;
      this.projectionMatrix = null;
      this.getProjectionMatrix(epsilon);
      return this;
    }
    lookFrom(eyePoint, upVector = null, epsilon = EPSILON) {
      this.eyePoint = eyePoint;
      if (upVector !== null) {
        this.upVector = upVector;
      }
      this.projectionMatrix = null;
      this.getProjectionMatrix(epsilon);
      return this;
    }
    getProjectionMatrix(epsilon = EPSILON) {
      const zDirection = M(this.lookAtPoint, this.eyePoint);
      const length = g(zDirection);
      if (length < epsilon) {
        throw new Error("Eye point and look at point are too close together.");
      }
      const zNormalized = B(zDirection);
      var upComponent = perpendicularComponent(zNormalized, this.upVector);
      if (g(upComponent) < epsilon) {
        upComponent = perpendicularComponent(zNormalized, [1, 1, 0]);
      }
      this.upVector = B(upComponent);
      this.focusLength = length;
      this.zscale = length;
      this.projectionMatrix = ProjectionMatrix(this.eyePoint, this.lookAtPoint, this.upVector, epsilon);
      return this.projectionMatrix;
    }
    /** Rotate the projection by moving the eye point around the lookAt point.
     * @param rotationMatrix3d - The rotation matrix to apply in projected space.
     */
    rotation(rotationMatrix3d) {
      const upVector = this.upVector;
      const lookAtPoint = this.lookAtPoint;
      const eyePoint = this.eyePoint;
      const orientation = this.orientation();
      const inverseOrientation = G(orientation);
      const orientProjection = T(rotationMatrix3d, orientation);
      const oriented = T(inverseOrientation, orientProjection);
      const newUpVector = $(oriented, upVector);
      const offset = M(eyePoint, lookAtPoint);
      const newoffset = $(oriented, offset);
      const newEyePoint = p(lookAtPoint, newoffset);
      const result = new Projector(newEyePoint, lookAtPoint, this.perspective, newUpVector);
      return result;
    }
    distanceScale(atPoint) {
      const toPoint = M(atPoint, this.eyePoint);
      const distance = g(toPoint);
      if (distance < EPSILON) {
        return 1;
      }
      const scale = this.focusLength / distance;
      return scale;
    }
    /** 3x3 3d rotation matrix based on xy offset adjusted by focuslength  */
    XYOffsetRotation(startXY, endXY) {
      const offset = M(endXY, startXY);
      const [dx, dy] = offset;
      const focusLength = this.focusLength;
      const rotation = this.rotateYawPitch(-dx / focusLength, -dy / focusLength);
      return rotation;
    }
    /* not used
    rotateXY(startXY: tsvector.Vector, endXY: tsvector.Vector, projectionMatrix: tsvector.Matrix | null): Projector {
        // Create a rotation matrix for the XY mouse offset
        const offset = tsvector.vSub(endXY, startXY);
        const [dx, dy] = offset;
        const focusLength = this.focusLength;
        //("Focus Length:", focusLength, "Offset:", offset);
        //const affineRotation = OrbitRotation([dx / focusLength, dy / focusLength]);
        const rotation = this.rotateYawPitch(dx / focusLength, dy / focusLength);
        const affineRotation = tsvector.affine3d(rotation);
        return this.rotate(affineRotation, projectionMatrix);
    };
    */
    rotateYawPitch(pitch, yaw) {
      const Myaw = J(-yaw);
      const Mpitch = K(-pitch);
      const rotated = T(Mpitch, Myaw);
      return rotated;
    }
    /** Rotate the projection matrix by the given affine rotation matrix at the lookAtPoint.
     * @param affineRotation - The affine rotation matrix to apply.
     * @param projectionMatrix - Optional, if not provided, will use the current projection matrix.
     */
    /* not used ???
    rotate(affineRotation: tsvector.Matrix, projectionMatrix: tsvector.Matrix | null = null): Projector {
        if (projectionMatrix === null) {
            if (this.projectionMatrix === null) {
                this.getProjectionMatrix();
            }
            projectionMatrix = this.projectionMatrix;
        }
        // projectionMatrix is currently at the eyePoint
        // Apply the rotation at the lookAtPoint and then translate back to the eyePoint
        const shift = tsvector.vSub(this.eyePoint, this.lookAtPoint);
        const translateToLookAt = tsvector.affine3d(null, shift);
        const translated = tsvector.MMProduct(translateToLookAt, projectionMatrix!);
        const rotated = tsvector.MMProduct(affineRotation, translated);
        const invRotation = tsvector.MInverse(affineRotation);
        const rotatedShiftAffine = tsvector.MvProduct(invRotation, affine3d(shift));
        const rotatedShift = rotatedShiftAffine.slice(0, 3); // drop the last element
        const translateBack = tsvector.affine3d(null, tsvector.vScale(-1, rotatedShift));
        this.projectionMatrix = tsvector.MMProduct(translateBack, rotated);
        return this;
    };
    */
    orientation() {
      if (this.projectionMatrix === null) {
        this.getProjectionMatrix();
      }
      const projection2 = this.projectionMatrix;
      return [
        projection2[0].slice(0, 3),
        projection2[1].slice(0, 3),
        projection2[2].slice(0, 3)
      ];
    }
    project(xyz) {
      if (this.projectionMatrix === null) {
        this.getProjectionMatrix();
      }
      const affine = affine3d(xyz);
      const projected = $(this.projectionMatrix, affine);
      projected[2] /= this.zscale;
      const P2 = [projected[0] / projected[3], projected[1] / projected[3], projected[2] / projected[3]];
      if (this.perspective) {
        const scale = 1 / P2[2];
        return [P2[0] * scale, P2[1] * scale, P2[2]];
      } else {
        return [P2[0], P2[1], P2[2]];
      }
    }
  }
  const projection = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    ProjectionMatrix,
    Projector,
    affine3d,
    perpendicularComponent
  }, Symbol.toStringTag, { value: "Module" }));
  let Image$1 = class Image extends Rectangle {
    constructor(source, frame2, point, size = null, offset = [0, 0], scaled = false) {
      super(frame2, point, size, offset, scaled);
      __publicField(this, "source");
      __publicField(this, "awaitingLoad", false);
      this.source = source;
      this.checkCompletion(source);
    }
    async checkCompletion(image) {
      if (image.complete && image.naturalWidth !== 0) {
        if (this.size === null) {
          this.size = [image.naturalWidth, image.naturalHeight];
        }
      } else {
        this.awaitingLoad = true;
        return new Promise((resolve, reject) => {
          image.onload = () => {
            if (this.size === null) {
              this.size = [image.naturalWidth, image.naturalHeight];
            }
            if (this.awaitingLoad) {
              this.awaitingLoad = false;
              this.requestRedraw();
            }
            resolve();
          };
          image.onerror = () => {
            reject(new Error("Failed to load image."));
          };
        });
      }
    }
    drawPath() {
      if (!this.isLive()) {
        throw new Error("Image is not attached to a frame.");
      }
      if (this.size === null) {
        this.awaitingLoad = true;
        return new Path2D();
      }
      return super.drawPath();
    }
    // override draw to draw the image
    draw() {
      if (!this.isLive()) {
        return;
      }
      if (this.size === null) {
        this.awaitingLoad = true;
        return;
      }
      this.drawPath();
      this.prepare();
      const frame2 = this.onFrame;
      const ctx = frame2.diagram.ctx;
      const pixelPoint = frame2.toPixel(this.point);
      const canvasPoint = frame2.diagram.toCanvas(pixelPoint);
      const rotation = new Rotation2d(-this.rotationDegrees, canvasPoint);
      rotation.applyToCanvas(ctx);
      let pixelStart;
      let pixelSize;
      ({ pixelStart, pixelSize } = this.getPixelStartAndSize());
      const [px, py] = pixelStart;
      const [pw, ph] = pixelSize;
      const [cx, cy] = [px, frame2.diagram.canvas.height - py];
      const imagey = cy - ph;
      ctx.drawImage(this.source, cx, imagey, pw, ph);
      ctx.restore();
    }
  };
  class TextBox extends Rectangle {
    constructor(text, frame2, point, shift = [0, 0], alignment = "left", background = null) {
      const dummyoffset = [0, 0];
      super(frame2, point, null, dummyoffset, false);
      __publicField(this, "text");
      __publicField(this, "background");
      __publicField(this, "referencePoint");
      __publicField(this, "shift");
      __publicField(this, "alignment");
      __publicField(this, "valignment", "alphabetic");
      this.text = text;
      this.background = background;
      this.referencePoint = point;
      this.alignment = alignment;
      this.shift = shift;
    }
    // use the reference point for get/set operations
    getFramePoint() {
      return this.referencePoint;
    }
    setFramePoint(position) {
      this.referencePoint = position;
    }
    // setters
    valigned(valignment) {
      this.valignment = valignment;
      this.requestRedraw();
      return this;
    }
    setText(text) {
      this.text = text;
      this.requestRedraw();
      return this;
    }
    setShift(shift) {
      this.shift = shift;
      this.requestRedraw();
      return this;
    }
    aligned(alignment) {
      this.alignment = alignment;
      this.requestRedraw();
      return this;
    }
    boxed(background) {
      this.background = background;
      this.requestRedraw();
      return this;
    }
    // override draw to draw the text box
    draw() {
      if (!this.isLive()) {
        return;
      }
      const frame2 = this.onFrame;
      const ctx = frame2.diagram.ctx;
      this.prepare();
      const bgPath = this.drawPath();
      ctx.textAlign = this.alignment;
      ctx.textBaseline = this.valignment;
      if (this.textFont) {
        ctx.font = this.textFont;
      }
      if (this.background) {
        ctx.fillStyle = this.background;
        ctx.fill(bgPath);
      }
      const shiftedPoint = p(this.referencePoint, this.shift);
      const pixelPos = this.onFrame.toPixel(shiftedPoint);
      const canvasPos = this.onFrame.diagram.toCanvas(pixelPos);
      const [x2, y2] = canvasPos;
      const rotation = new Rotation2d(-this.rotationDegrees, canvasPos);
      rotation.applyToCanvas(ctx);
      ctx.fillStyle = this.color;
      ctx.fillText(this.text, x2, y2);
      ctx.restore();
    }
    // compute path for background rectangle
    drawPath() {
      if (!this.isLive()) {
        throw new Error("TextBox is not attached to a frame.");
      }
      const { offset, size } = this.getSize();
      this.point = p(this.referencePoint, this.shift);
      this.size = size;
      this.offset = offset;
      this.scaled = false;
      return super.drawPath();
    }
    // get the size of the text box in pixels and the offset of the lower left corner
    getSize() {
      if (!this.isLive()) {
        throw new Error("TextBox is not attached to a frame.");
      }
      const ctx = this.onFrame.diagram.ctx;
      if (this.textFont) {
        ctx.save();
        ctx.font = this.textFont;
      }
      const m2 = ctx.measureText(this.text);
      if (this.textFont) {
        ctx.restore();
      }
      const textWidth = m2.width;
      const textHeight = m2.actualBoundingBoxAscent + m2.actualBoundingBoxDescent;
      const heightrescale = 1.5;
      const textHeightPadded = textHeight * heightrescale;
      const size = [textWidth, textHeightPadded];
      let offsety = -m2.actualBoundingBoxDescent;
      let offsetx = -m2.actualBoundingBoxLeft;
      if (this.alignment === "center") {
        offsetx = offsetx - textWidth / 2;
      } else if (this.alignment === "right") {
        offsetx = offsetx - textWidth;
      }
      if (this.valignment === "top") {
        offsety = offsety - textHeight;
      } else if (this.valignment === "middle") {
        offsety = offsety - textHeight / 2;
      } else if (this.valignment === "alphabetic") ;
      else if (this.valignment === "ideographic") ;
      else if (this.valignment === "bottom") ;
      const offset = [offsetx, offsety];
      return { offset, size };
    }
  }
  class Assembly extends Marking {
    constructor(onFrame) {
      super(onFrame);
      // the dedicated frame for drawing this assembly.
      __publicField(this, "assemblyFrame");
      // reference point
      __publicField(this, "framePoint", [0, 0]);
      this.assemblyFrame = new Frame(onFrame.diagram, null, onFrame);
      this.setTranslation(this.framePoint);
      onFrame.addElement(this.assemblyFrame);
    }
    // The prepare operation makes the assembly
    prepareForRedraw() {
      const assemblyFrame = this.assemblyFrame;
      assemblyFrame.clear();
      assemblyFrame.styleLike(this);
      this.assemble(assemblyFrame);
    }
    setTranslation(position) {
      this.framePoint = position;
      const reverse = v(-1, position);
      const translationMatrix = translateScaleMatrix(reverse, null);
      this.assemblyFrame.setAffine(translationMatrix);
    }
    setFramePoint(position) {
      this.setTranslation(position);
      this.requestRedraw();
    }
    getFramePoint() {
      return this.framePoint;
    }
    pickObject(canvasXY) {
      const picked = this.assemblyFrame.pickedMarkings(canvasXY);
      if (picked.length > 0) {
        return true;
      } else {
        return false;
      }
    }
    drawPath() {
      return new Path2D();
    }
    draw() {
    }
  }
  class Star extends Assembly {
    constructor(onFrame, center, innerRadius, numPoints = 5, pointFactor = 1.4, degrees = 0) {
      super(onFrame);
      __publicField(this, "center", [0, 0]);
      __publicField(this, "numPoints");
      __publicField(this, "innerRadius");
      __publicField(this, "outerRadius");
      __publicField(this, "rotationDegrees");
      this.numPoints = numPoints;
      this.innerRadius = innerRadius;
      this.outerRadius = innerRadius * pointFactor;
      this.rotationDegrees = degrees;
      this.setTranslation(center);
    }
    assemble(onFrame) {
      const center = [0, 0];
      const radiansPerPoint = 2 * Math.PI / (this.numPoints * 2);
      const points = [];
      const rotationRadians = this.rotationDegrees * Math.PI / 180;
      for (let i = 0; i < this.numPoints * 2; i++) {
        const radius = i % 2 === 0 ? this.outerRadius : this.innerRadius;
        const angle = i * radiansPerPoint + rotationRadians;
        const x2 = center[0] + radius * Math.cos(angle);
        const y2 = center[1] + radius * Math.sin(angle);
        points.push([x2, y2]);
      }
      const poly2 = onFrame.polygon(points);
      poly2.closed(true);
      poly2.styleLike(this);
      poly2.filled();
    }
  }
  class Arrow extends Assembly {
    // fraction of length if tipLength is null
    constructor(onFrame, back, tip, tipLength = null, tipDegrees = 20, tipFactor = 0.1) {
      super(onFrame);
      __publicField(this, "back");
      __publicField(this, "tip");
      __publicField(this, "vector");
      __publicField(this, "tipDegrees", 20);
      __publicField(this, "tipLength", 10);
      __publicField(this, "tipFactor", 0.1);
      this.back = back;
      this.tip = tip;
      this.vector = M(tip, back);
      this.tipDegrees = tipDegrees;
      this.tipLength = tipLength;
      this.tipFactor = tipFactor;
      this.setTranslation(back);
    }
    assemble(onFrame, epsilon = 1e-5) {
      const vecLength = g(this.vector);
      let tipLength = this.tipLength;
      if (vecLength < epsilon) {
        return;
      }
      if (tipLength === null) {
        tipLength = this.tipFactor * vecLength;
      }
      const unitVector = v(1 / vecLength, this.vector);
      const perpVector = [-unitVector[1], unitVector[0]];
      const radians = this.tipDegrees * Math.PI / 180;
      const c2 = Math.cos(radians);
      const s2 = Math.sin(radians);
      const orthComponent = v(s2 * tipLength, perpVector);
      const negComponent = v(-c2 * tipLength, unitVector);
      const offsetA = p(negComponent, orthComponent);
      const tipA = p(offsetA, this.vector);
      const offsetB = M(negComponent, orthComponent);
      const tipB = p(offsetB, this.vector);
      const points = [];
      points.push([0, 0]);
      points.push(this.vector);
      points.push(tipA);
      points.push(this.vector);
      points.push(tipB);
      const poly2 = onFrame.polygon(points);
      poly2.styleLike(this);
      poly2.stroked();
      poly2.closed(false);
      poly2.join("round");
    }
  }
  function translateScaleMatrix(translate, scale) {
    if (translate === null) {
      translate = [0, 0];
    }
    if (scale === null) {
      scale = [1, 1];
    }
    return [
      [scale[0], 0, translate[0]],
      [0, scale[1], translate[1]],
      [0, 0, 1]
    ];
  }
  function regionMap(fromMinxy, fromMaxxy, toMinxy, toMaxxy) {
    const fromSize = M(fromMaxxy, fromMinxy);
    const toSize = M(toMaxxy, toMinxy);
    const scale = Z(toSize, fromSize);
    const translateToOrigin = translateScaleMatrix(v(-1, fromMinxy), [1, 1]);
    const scaleMatrix = translateScaleMatrix([0, 0], scale);
    const translateToDestination = translateScaleMatrix(toMinxy, [1, 1]);
    return T(
      translateToDestination,
      T(scaleMatrix, translateToOrigin)
    );
  }
  function applyAffine(affine, xy) {
    const v3 = $(affine, [...xy, 1]);
    return [v3[0], v3[1]];
  }
  const identity = w(3);
  class Frame extends Styled {
    // event handlers for frame events
    //typeToEventHandler: Map<string, frameEventHandler> = new Map();
    constructor(inDiagram, affineMatrix = null, parent = null, font = "12px Arial") {
      super(parent);
      __publicField(this, "diagram");
      // convert from parent model to local model
      __publicField(this, "affine", identity);
      // convert from local model to parent model
      __publicField(this, "inv", identity);
      // convert from cartesian pixel to local model
      __publicField(this, "pixelToModel", identity);
      // convert from local model to cartesian pixel
      __publicField(this, "ModelToPixel", identity);
      // record of all markings
      __publicField(this, "nameToMarking", /* @__PURE__ */ new Map());
      // draw ordered markings
      __publicField(this, "drawOrder", []);
      this.diagram = inDiagram;
      this.onFrame = parent;
      if (affineMatrix === null) {
        affineMatrix = identity;
      }
      this.setAffine(affineMatrix);
      this.responsive = true;
      this.font(font);
    }
    /** The pixel position is the frame origin in pixel coordinates.
     * @return The pixel position of the frame origin.
     */
    getPixel() {
      return this.toPixel([0, 0]);
    }
    /** translate the origin to a new pixel position.
     * @param position The new pixel position of the frame origin.
     */
    setPixel(position) {
      const model = this.toModel(position);
      const shift = v(-1, model);
      const translation = translateScaleMatrix(shift, null);
      const newAffine = T(translation, this.affine);
      this.setAffine(newAffine);
    }
    /** handle a mouse event.
     * @internal
     * @param event The mouse event to handle.
     * @param canvasXY The canvas coordinates of the mouse event.
     * @param cartesianXY The cartesian pixel coordinates of the mouse event.
     * @returns True if the event was handled, false otherwise.
     */
    frameEventHandler(event, canvasXY, cartesianXY) {
      return this.mouseEventHandler(event.type, canvasXY, cartesianXY, [0, 0]);
    }
    /** handle a mouse event.
     * @internal
     * @param eventtype The type of the event (e.g., "click", "mousemove").
     * @param canvasXY The coordinates of the event in canvas pixels.
     * @param cartesianXY The coordinates of the event in cartesian pixels.
     * @param frameXY0 The coordinates of the event in the frame's local coordinate system.
     * @returns True if the event was handled, false otherwise.
     */
    mouseEventHandler(eventtype, canvasXY, cartesianXY, frameXY0) {
      let handled = false;
      const frameXY = this.toModel(cartesianXY);
      handled = super.mouseEventHandler(eventtype, canvasXY, cartesianXY, frameXY);
      if (!handled) {
        const picked = this.pickedMarkings(canvasXY);
        while (picked.length > 0 && !handled) {
          const element = picked.pop();
          if (element) {
            handled = element.mouseEventHandler(eventtype, canvasXY, cartesianXY, frameXY);
          }
        }
      }
      return handled;
    }
    /** Return all responsive markings that are picked by the canvas coordinates, in reverse draw order (topmost first)
     * @internal
    * @param canvasXY The coordinates in canvas pixels to test for picking.
    * @returns An array of responsive styled elements that are picked, in reverse draw order (topmost first).
    */
    pickedMarkings(canvasXY) {
      const result = [];
      for (const element of this.drawOrder) {
        if (element.responsive && element.pickObject(canvasXY)) {
          result.push(element);
        }
      }
      return result;
    }
    /** Rename a styled element in this frame and the containing diagram.
     * @param element The styled element to rename.
     * @param newName The new name for the element.
     */
    renameElement(element, newName) {
      const n2m = this.nameToMarking;
      if (n2m.has(newName)) {
        throw new Error(`Element name ${newName} already exists in frame ${this.objectName}`);
      }
      const oldName = element.objectName;
      if (n2m.has(oldName)) {
        const diagram2 = this.diagram;
        if (diagram2.getStyledByName(oldName) === null) {
          throw new Error(`Element ${oldName} not found in diagram during rename.`);
        }
        diagram2.deleteStyled(element);
        n2m.delete(oldName);
        element.objectName = newName;
        n2m.set(newName, element);
        diagram2.addStyled(element);
      } else {
        console.warn(`Element ${oldName} not found in frame ${this.objectName}`);
      }
    }
    /** Clear all elements from frame, forgetting them and removing from draw order and name map. */
    clear() {
      this.nameToMarking.forEach((element) => {
        element.forget();
      });
      this.nameToMarking.clear();
      this.drawOrder = [];
      this.diagram.requestRedraw();
    }
    /** Receive canvas events of this eventType.
     * @param eventType String name of event to recieve.
     */
    watchEvent(eventType) {
      this.diagram.watchEvent(eventType);
    }
    /** Make an image usable in a diagram by name.
     * @param name The name to associate with the image.
     * @param image The HTMLImageElement to name.
     * @returns The current frame for chaining.
     */
    nameImage(name2, image2) {
      this.diagram.nameImage(name2, image2);
      return this;
    }
    /** Make an image from a URL usable in a diagram by name.
     * @param name The name to associate with the image.
     * @param url The URL of the image to load and name.
     * @returns The current frame for chaining.
     */
    nameImageFromURL(name2, url) {
      this.diagram.nameImageFromURL(name2, url);
      return this;
    }
    /** Fit visible elements into canvas.
     * @param border Optional border in cartesian units to leave around fitted elements.  Default is 0.
     */
    fit(border = 0) {
      this.diagram.fit(border);
      this.requestRedraw();
    }
    /** Record a cartesian pixel point and convert to canvas coords.
     * @internal
     * @param xy The cartesian pixel coordinates of the point to add.
     * @returns The canvas coordinates of the added point.
    */
    addPixelPoint(xy) {
      const diagram2 = this.diagram;
      const [x2, y2] = xy;
      diagram2.addxy(x2, y2);
      return diagram2.toCanvas(xy);
    }
    /**
     * Request a redraw of the diagram.
     */
    requestRedraw() {
      this.diagram.requestRedraw();
    }
    /** Pause automatic redraws of the diagram (in case of extensive updates) */
    pauseRedraw() {
      this.diagram.pauseRedraw();
    }
    /** Resume automatic redraws of the diagram, possibly after a pause */
    resumeRedraw() {
      this.diagram.resumeRedraw();
    }
    /** Add a model point, record its cartesian pixel coords and convert to canvas.
     * @internal
     * @param xy The model coordinates of the point to add.
     * @returns The canvas coordinates of the added point.
     */
    addPoint(xy) {
      const pixel = this.toPixel(xy);
      return this.addPixelPoint(pixel);
    }
    /** Add a canvas pixel point, record its cartesian pixel coords and return frame model point.
     * @param xy The canvas coordinates of the point to add.
     * @return The model coordinates of the added point.
     * @internal
    */
    addPixel(xy) {
      const diagram2 = this.diagram;
      const cartesian = diagram2.toCartesian(xy);
      const model = this.toModel(cartesian);
      diagram2.addPoint(cartesian);
      return model;
    }
    /** Set the affine transformation matrix from parent frame to this frame.
     * @param affineMatrix The affine transformation matrix to set.
     */
    setAffine(affineMatrix) {
      this.affine = affineMatrix;
      this.inv = G(affineMatrix);
      this.requestRedraw();
    }
    /**
     * Sync the pixel and model coordinate systems with the parent frame.
     * @internal
     */
    prepareForRedraw() {
      this.pixelToModel = this.affine;
      this.ModelToPixel = this.inv;
      let parent = this.onFrame;
      if (parent !== null) {
        this.pixelToModel = T(this.affine, parent.pixelToModel);
        this.ModelToPixel = T(parent.ModelToPixel, this.inv);
      }
      this.nameToMarking.forEach((element) => {
        element.prepareForRedraw();
      });
    }
    /** Convert from model space to cartesian pixel space.
     * @param xy The model coordinates to convert.
     * @returns The cartesian pixel coordinates.
     * @internal
     */
    toPixel(xy) {
      return applyAffine(this.ModelToPixel, xy);
    }
    /** Convert from cartesian pixel space to model space
     * @param xy The cartesian pixel coordinates to convert.
     * @returns The model coordinates.
     * @internal
     */
    toModel(xy) {
      return applyAffine(this.pixelToModel, xy);
    }
    /** Create a frame for a subregion and record it. 
     * fromMinxy..fromMaxxy is the region in the current frame.
     * toMinxy..toMaxxy is the region in the new frame.
     * @param fromMinxy The minimum xy coordinates in the parent frame.
     * @param fromMaxxy The maximum xy coordinates in the parent frame.
     * @param toMinxy The minimum xy coordinates in the new frame.
     * @param toMaxxy The maximum xy coordinates in the new frame.
     * @return The new frame.
    */
    regionFrame(fromMinxy, fromMaxxy, toMinxy, toMaxxy) {
      const affine = regionMap(fromMinxy, fromMaxxy, toMinxy, toMaxxy);
      const result = new Frame(this.diagram, affine, this);
      this.addElement(result);
      return result;
    }
    /**
     * Create a 3d frame from a projection.
     * @internal
     * @param project The projection for the 3d frame.
     * @returns A new 3d frame attached to this 2d frame.
     */
    projectionFrame(project) {
      const result = new Frame3d(this, project);
      this.addElement(result);
      return result;
    }
    /**
     * Create a 3d frame attached to this 2d frame.
     * @param eyePoint The "view origin" of the 3d projection.
     * @param lookAtPoint The "focus" of the 3d projection view.
     * @param perspective Whether to use perspective (true) or orthographic viewing (false)
     * @param upVector The "up" direction of the 3d projection view. Defaults to (0, 0, 1)
     * @returns A new 3d frame attached to this 2d frame.
     */
    frame3d(eyePoint, lookAtPoint, perspective = true, upVector = null) {
      const projector = new Projector(eyePoint, lookAtPoint, perspective, upVector);
      return this.projectionFrame(projector);
    }
    /**
     * Get a styled object from this diagram by name (convenience)
     * @param name 
     * @returns styled.Styled
     */
    getStyledByName(name2) {
      return this.diagram.getStyledByName(name2);
    }
    /** Record a marking.
     * @internal
     * @param styled The styled marking to add.
     * @param requestRedraw Whether to request a redraw after adding the element (default: true).   
     */
    addElement(styled2, requestRedraw = true) {
      const name2 = styled2.objectName;
      const diagram2 = this.diagram;
      diagram2.resetStats();
      diagram2.addStyled(styled2);
      this.nameToMarking.set(name2, styled2);
      this.drawOrder.push(styled2);
      if (requestRedraw) {
        this.requestRedraw();
      }
    }
    /** iterate over all markings to draw.
     * @internal
     */
    draw() {
      let dirty = false;
      const ctx = this.diagram.ctx;
      ctx.save();
      this.applyStyle(ctx);
      for (const element of this.drawOrder) {
        if (element.defunct) {
          dirty = true;
        } else {
          element.draw();
        }
      }
      ctx.restore();
      if (dirty) {
        let diagram2 = this.diagram;
        let n2m = this.nameToMarking;
        let newOrder = [];
        for (const element of this.drawOrder) {
          if (!element.defunct) {
            newOrder.push(element);
          } else {
            n2m.delete(element.objectName);
            diagram2.deleteStyled(element);
          }
        }
        this.drawOrder = newOrder;
      }
    }
    /** line between two end points.
     * @param start The starting point of the line in model coordinates.
     * @param end The ending point of the line in model coordinates.
     * @returns The created line marking.   
     */
    line(start, end) {
      const result = new Line(this, start, end);
      this.addElement(result);
      return result;
    }
    /** A dot is a circle with an unscaled radius.
     * @param center The center of the dot in model coordinates.
     * @param radius The radius of the dot in model units.
     * @param scaled Whether the radius is scaled (default: false).
     * @returns The created circle marking.
    */
    dot(center, radius, scaled = false) {
      const result = new Circle(this, center, radius, scaled);
      this.addElement(result);
      return result;
    }
    /** A circle is a circle with a scaled radius.
     * @param center The center of the circle in model coordinates.
     * @param radius The radius of the circle in model units.
     * @param scaled Whether the radius is scaled (default: true).
     * @returns The created circle marking.
    */
    circle(center, radius, scaled = true) {
      return this.dot(center, radius, scaled);
    }
    /** Place a named image.
     * @param point The location of the image in model coordinates.
     * @param name The name of the image to place.
     * @param size The size of the image in model units or pixels if not scaled(default: null for natural size).
     * @param offset The offset of the image from the point in model units (default: [0,0]).
     * @param scaled Whether the size is scaled (default: false).
     * @returns The created image marking.
    */
    namedImage(point, name2, size = null, offset = [0, 0], scaled = false) {
      const source = this.diagram.getNamedImage(name2);
      if (source === null) {
        throw new Error(`Named image ${name2} not found in diagram.`);
      }
      const result = new Image$1(source, this, point, size, offset, scaled);
      this.addElement(result);
      return result;
    }
    /** A rectangle marking.
     * @param point The location of the rectangle in model coordinates.
     * @param size The size of the rectangle in model units (or pixels if not scaled).
     * @param offset The offset of the rectangle from the point in model units (default: [0,0]).
     * @param scaled Whether the size is scaled (default: true).
     * @param rotationDegrees The rotation of the rectangle in degrees (default: 0).
     * @returns The created rectangle marking.
    */
    rect(point, size, offset = [0, 0], scaled = true, rotationDegrees = 0) {
      const result = new Rectangle(this, point, size, offset, scaled, rotationDegrees);
      this.addElement(result);
      return result;
    }
    /** A text box. */
    textBox(point, text, shift = [0, 0], alignment = "left", background = null) {
      const result = new TextBox(text, this, point, shift, alignment, background);
      this.addElement(result);
      return result;
    }
    /** A box is an unscaled rectangle.
     * @param point The location of the box in model coordinates.
     * @param size The size of the box in pixels.
     * @param offset The offset of the box from the point in pixels (default: [0,0]).
     * @param scaled Whether the size is scaled (default: false).
     * @returns The created rectangle marking.
     */
    box(point, size, offset = [0, 0], scaled = false) {
      return this.rect(point, size, offset, scaled);
    }
    /** A square is a centered unscaled rectangle with equal sides.
     * @param point The location of the square in model coordinates.
     * @param size The size of the square sides in pixels.
     * @param offset The offset of the square from the point in pixels (default: null for centered).
     * @param scaled Whether the size is scaled (default: false).
     * @returns The created rectangle marking.
     */
    square(point, size, offset = null, scaled = false) {
      const result = Square(this, point, size, offset, scaled);
      this.addElement(result);
      return result;
    }
    /** a polyline is a poly that is stroked and not closed,
     * @param points The points of the polyline in model coordinates.
     * @returns The created polyline marking.
     */
    polyline(points) {
      const result = new Poly(this, points);
      result.closed(false).stroked();
      this.addElement(result);
      return result;
    }
    /** a polygon is a poly that is filled and closed,
     * @param points The points of the polygon in model coordinates.
     * @returns The created polygon marking.
     */
    polygon(points) {
      const result = new Poly(this, points);
      result.closed().filled();
      this.addElement(result);
      return result;
    }
    /** A star shape.
     * @param innerRadius The inner radius of the star.
     * @param numPoints The number of points of the star (default: 5).
     * @param pointFactor The factor by which the outer radius exceeds the inner radius (default: 1.4).
     * @param degrees The rotation of the star in degrees (default: 0).
     * @returns The created star marking.
     */
    star(center, innerRadius, numPoints = 5, pointFactor = 2, degrees = 0) {
      const result = new Star(this, center, innerRadius, numPoints, pointFactor, degrees);
      this.addElement(result);
      return result;
    }
    arrow(back, tip, tipDegrees = 30, tipLength = null, tipFactor = 0.1) {
      const result = new Arrow(this, back, tip, tipLength, tipDegrees, tipFactor);
      this.addElement(result);
      return result;
    }
  }
  const frame = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    Frame,
    applyAffine,
    regionMap,
    translateScaleMatrix
  }, Symbol.toStringTag, { value: "Module" }));
  function drawOn(container, width, height) {
    const diag = new Diagram(container, width, height);
    return diag.mainFrame;
  }
  class Diagram {
    constructor(domObject, width, height) {
      // The container for the canvas
      __publicField(this, "container");
      __publicField(this, "width");
      __publicField(this, "height");
      __publicField(this, "canvas");
      __publicField(this, "ctx");
      // Record of coordinate extremes in cartesian coordinates
      __publicField(this, "stats");
      __publicField(this, "last_stats", null);
      // The primary frame for the diagram
      __publicField(this, "mainFrame");
      __publicField(this, "nameToImage");
      __publicField(this, "redraw_requested", false);
      __publicField(this, "deferred_fit_border", null);
      __publicField(this, "autoRedraw", true);
      __publicField(this, "watchedEvents", /* @__PURE__ */ new Set());
      // for external named access, keep track of named styled elements
      __publicField(this, "nameToStyled", /* @__PURE__ */ new Map());
      this.container = domObject;
      this.width = width;
      this.height = height;
      this.nameToImage = /* @__PURE__ */ new Map();
      this.canvas = document.createElement("canvas");
      this.canvas.width = width;
      this.canvas.height = height;
      this.canvas.style.border = "1px solid black";
      this.container.innerHTML = "";
      this.container.appendChild(this.canvas);
      this.ctx = this.canvas.getContext("2d");
      this.stats = new CanvasStats();
      this.last_stats = this.stats;
      this.mainFrame = new Frame(this, null, null);
    }
    /** Get a styled object associated with the diagram by name.
     * @param name The name of the styled object.
     * @returns The styled object or null if not found.
    */
    getStyledByName(name2) {
      const styled2 = this.nameToStyled.get(name2);
      if (styled2 === void 0) {
        return null;
      }
      return styled2;
    }
    /** Add a styled object to the diagram's name registry.
     * @param styled The styled object to add
     * @internal
    */
    addStyled(styled2) {
      const n2s = this.nameToStyled;
      const existing = n2s.get(styled2.objectName);
      if (existing !== void 0) {
        if (existing === styled2) {
          return;
        }
        throw new Error(`Styled object name ${styled2.objectName} already exists in diagram.`);
      }
      n2s.set(styled2.objectName, styled2);
    }
    /** Delete a styled object from the diagram's name registry.
     * @param styled The styled object to delete
     * @internal
    */
    deleteStyled(styled2) {
      const n2s = this.nameToStyled;
      if (n2s.has(styled2.objectName)) {
        n2s.delete(styled2.objectName);
      }
    }
    /** Event handler for any mouse event 
     * @param event The mouse event to handle.
     * @internal
    */
    mouseEventHandler(event) {
      const rect2 = this.canvas.getBoundingClientRect();
      const x2 = event.clientX - rect2.left;
      const y2 = event.clientY - rect2.top;
      const canvasXY = [x2, y2];
      const cartesianXY = this.toCartesian(canvasXY);
      this.mainFrame.frameEventHandler(event, canvasXY, cartesianXY);
    }
    /** handle an event of a given type 
     * @param eventType The type of the event to watch.
     * @returns The diagram for chaining.
     * @internal
    */
    watchEvent(eventType) {
      if (this.watchedEvents.has(eventType)) {
        return this;
      }
      if (this.ctx === null) {
        throw new Error("Canvas context is not available.");
      }
      this.canvas.addEventListener(eventType, (event) => {
        this.mouseEventHandler(event);
      });
      return this;
    }
    /** set image smoothing.
     * @param smooth - true to enable smoothing, false to disable.
     * @returns The diagram for chaining.
    */
    smoothImages(smooth = true) {
      if (this.ctx === null) {
        return;
      }
      this.ctx.imageSmoothingEnabled = smooth;
      return this;
    }
    /** Make an image usable in a diagram by name. 
     * @param name The name to assign to the image.
     * @param image The HTMLImageElement to name.
     * @returns The diagram for chaining.
    */
    nameImage(name2, image) {
      this.nameToImage.set(name2, image);
      return this;
    }
    /** Get a named image from the diagram. 
     * @param name The name of the image.
     * @returns The HTMLImageElement or null if not found.
    */
    getNamedImage(name2) {
      const image = this.nameToImage.get(name2);
      if (image === void 0) {
        return null;
      }
      return image;
    }
    /** Make an image from a URL usable in a diagram by name. 
     * @param name The name to assign to the image.
     * @param url The URL of the image.
     * @returns The diagram for chaining.
    */
    nameImageFromURL(name2, url) {
      const image = new Image();
      image.src = url;
      this.nameImage(name2, image);
    }
    /** Convert cartesian xy to canvas xy (with y inverted) 
     * @internal
     * @param xy The cartesian coordinates to convert.
     * @returns The corresponding canvas coordinates.
    */
    toCanvas(xy) {
      const result = [xy[0], this.height - xy[1]];
      return result;
    }
    /** Convert canvas xy to cartesian xy (with y inverted) 
     * @internal
     * @param xy The canvas coordinates to convert.
     * @returns The corresponding cartesian coordinates.
    */
    toCartesian(xy) {
      const result = [xy[0], this.height - xy[1]];
      return result;
    }
    /** Draw the diagram */
    draw() {
      this.clear();
      this.mainFrame.prepareForRedraw();
      this.mainFrame.draw();
      if (this.deferred_fit_border !== null) {
        const border = this.deferred_fit_border;
        this.fit(border);
        this.deferred_fit_border = null;
        this.requestRedraw();
      }
    }
    /** Request a redraw of the diagram */
    requestRedraw() {
      if (!this.redraw_requested) {
        this.redraw_requested = true;
        if (!this.autoRedraw) {
          return;
        }
        requestAnimationFrame(() => {
          try {
            this.redraw_requested = false;
            this.draw();
          } finally {
          }
        });
      }
    }
    /** Set the auto redraw flag */
    resumeRedraw() {
      if (this.autoRedraw) {
        return;
      }
      this.autoRedraw = true;
      if (this.redraw_requested) {
        this.redraw_requested = false;
        this.requestRedraw();
      }
    }
    /** Pause the auto redraw (in cases of large diagram updates) */
    pauseRedraw() {
      this.autoRedraw = false;
    }
    /** Clear the canvas and reset stats */
    clear() {
      this.ctx.clearRect(0, 0, this.width, this.height);
      this.last_stats = this.stats;
      this.resetStats();
    }
    /** Reset the drawing statistics 
     * @internal
    */
    resetStats() {
      this.stats = new CanvasStats();
    }
    /** record a cartesian xy point 
     * @internal
     * @param xy The cartesian coordinates of the point.
    */
    addPoint(xy) {
      this.stats.addPoint(xy);
    }
    addxy(x2, y2) {
      this.stats.addxy(x2, y2);
    }
    /** get pixels from the canvas
     * @param fromCanvasXY The top-left canvas coordinates of the region to get. If null, it will be [0, 0].
     * @param toCanvasXY The bottom-right canvas coordinates of the region to get.
     * If null, it will be [width, height].
     * @returns The ImageData object for the region.
     */
    getImageData(fromCanvasXY, toCanvasXY) {
      if (fromCanvasXY === null) {
        fromCanvasXY = [0, 0];
      }
      const [x2, y2] = fromCanvasXY;
      if (toCanvasXY === null) {
        toCanvasXY = [this.width, this.height];
      }
      const [width, height] = M(toCanvasXY, fromCanvasXY);
      return this.ctx.getImageData(x2, y2, width, height);
    }
    /** Get the rgba values from a pixel on the canvas primarily for testing.
    * @param canvasXY The canvas coordinates of the pixel.
    * @returns The rgba values as an array of four numbers.
    */
    getPixelData(canvasXY) {
      const [x2, y2] = canvasXY;
      const toCanvasXY = p(canvasXY, [1, 1]);
      const imageData = this.getImageData(canvasXY, toCanvasXY);
      const index = 0;
      return Array.from(imageData.data.slice(index, index + 4));
    }
    /** Use the draw statistics to fit the diagram to the visible points 
    * @param border The border to add around the fitted region in cartesian coordinates.
    */
    fit(border = 0) {
      if (this.stats.minxy === null || this.stats.maxxy === null) {
        this.deferred_fit_border = border;
        return;
      }
      const expander = [border, border];
      const minxy = M(this.stats.minxy, expander);
      const maxxy = p(this.stats.maxxy, expander);
      const width = this.width;
      const height = this.height;
      const diff = M(maxxy, minxy);
      const [dw, dh] = diff;
      if (dw === 0 || dh === 0) {
        return;
      }
      const aspect = dh / dw;
      const myAspect = height / width;
      let fromMinX = 0;
      let fromMaxX = width;
      let fromMinY = 0;
      let fromMaxY = height;
      if (aspect > myAspect) {
        const ddw = height / aspect;
        fromMinX = (width - ddw) / 2;
        fromMaxX = fromMinX + ddw;
      } else {
        const ddh = width * aspect;
        fromMinY = (height - ddh) / 2;
        fromMaxY = fromMinY + ddh;
      }
      const fromMinXY = [fromMinX, fromMinY];
      const fromMaxXY = [fromMaxX, fromMaxY];
      const affine = regionMap(minxy, maxxy, fromMinXY, fromMaxXY);
      const mainFrame = this.mainFrame;
      const currentAffine = mainFrame.ModelToPixel;
      const adjustedAffine = T(affine, currentAffine);
      const pixelToModel = G(adjustedAffine);
      mainFrame.setAffine(pixelToModel);
    }
  }
  class CanvasStats {
    constructor() {
      __publicField(this, "minxy");
      __publicField(this, "maxxy");
      this.minxy = null;
      this.maxxy = null;
    }
    addxy(x2, y2) {
      if (isNaN(x2) || isNaN(y2)) {
        throw new Error("Cannot add NaN values to stats");
      }
      this.addPoint([x2, y2]);
    }
    addPoint(point) {
      if (this.minxy === null) {
        this.minxy = point;
        this.maxxy = point;
      } else {
        this.minxy = b(this.minxy, point);
        this.maxxy = L(this.maxxy, point);
      }
    }
    overlaps(other) {
      if (this.minxy === null || this.maxxy === null) {
        return false;
      }
      if (other.minxy === null || other.maxxy === null) {
        return false;
      }
      const overlapMax = b(this.maxxy, other.maxxy);
      const overlapMin = L(this.minxy, other.minxy);
      const diff = M(overlapMax, overlapMin);
      return Math.min(...diff) > 0;
    }
  }
  const diagram = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    CanvasStats,
    Diagram,
    drawOn
  }, Symbol.toStringTag, { value: "Module" }));
  const name = "wassilyjs";
  exports2.circle = circle;
  exports2.conveniences = conveniences;
  exports2.cube = cube;
  exports2.diagram = diagram;
  exports2.drawOn = drawOn;
  exports2.frame = frame;
  exports2.frame3d = frame3d;
  exports2.line = line;
  exports2.line3d = line3d;
  exports2.marking = marking;
  exports2.marking3d = marking3d;
  exports2.name = name;
  exports2.panel = panel;
  exports2.poly = poly;
  exports2.poly3d = poly3d;
  exports2.projection = projection;
  exports2.rect = rect;
  exports2.styled = styled;
  exports2.swatch = swatch;
  exports2.tsvector = tsVector;
  Object.defineProperty(exports2, Symbol.toStringTag, { value: "Module" });
});
