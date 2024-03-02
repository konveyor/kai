/*! For license information please see 274.c892ae50.chunk.js.LICENSE.txt */
(self.webpackChunkkonveyor_static_report =
  self.webpackChunkkonveyor_static_report || []).push([
  [274],
  {
    55197: (t, e, n) => {
      "use strict";
      n.d(e, { k: () => fn });
      var r = {};
      n.r(r),
        n.d(r, {
          circle: () => ge,
          cross: () => Se,
          diamond: () => xe,
          minus: () => Ae,
          plus: () => Ce,
          square: () => be,
          star: () => je,
          triangleDown: () => Oe,
          triangleUp: () => we,
        });
      var o = n(75971),
        a = n(72791),
        i = n(62110),
        c = n.n(i),
        l = n(18425),
        u = n(66364),
        s = n.n(u),
        f = n(15687),
        p = n.n(f),
        d = n(66933),
        h = n.n(d),
        v = n(52007),
        y = n.n(v),
        m = n(78457),
        g = n(8091),
        b = n(97409),
        x = n(71472),
        O = n(70295),
        w = n(46577),
        C = n(42745),
        S = n(43350),
        A = ["desc"];
      function j() {
        return (
          (j = Object.assign
            ? Object.assign.bind()
            : function (t) {
                for (var e = 1; e < arguments.length; e++) {
                  var n = arguments[e];
                  for (var r in n)
                    Object.prototype.hasOwnProperty.call(n, r) && (t[r] = n[r]);
                }
                return t;
              }),
          j.apply(this, arguments)
        );
      }
      function k(t, e) {
        if (null == t) return {};
        var n,
          r,
          o = (function (t, e) {
            if (null == t) return {};
            var n,
              r,
              o = {},
              a = Object.keys(t);
            for (r = 0; r < a.length; r++)
              (n = a[r]), e.indexOf(n) >= 0 || (o[n] = t[n]);
            return o;
          })(t, e);
        if (Object.getOwnPropertySymbols) {
          var a = Object.getOwnPropertySymbols(t);
          for (r = 0; r < a.length; r++)
            (n = a[r]),
              e.indexOf(n) >= 0 ||
                (Object.prototype.propertyIsEnumerable.call(t, n) &&
                  (o[n] = t[n]));
        }
        return o;
      }
      var P = function (t) {
        var e = t.desc,
          n = k(t, A);
        return e
          ? a.createElement(
              "circle",
              j({ vectorEffect: "non-scaling-stroke" }, n),
              a.createElement("desc", null, e),
            )
          : a.createElement(
              "circle",
              j({ vectorEffect: "non-scaling-stroke" }, n),
            );
      };
      function E(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function M(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? E(Object(n), !0).forEach(function (e) {
                T(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : E(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function T(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      var _ = function (t) {
        return (t = (function (t) {
          var e = g.xs(t.id, t);
          return p()({}, t, { id: e });
        })(t)).polar
          ? a.cloneElement(
              t.circleComponent,
              M(
                M({}, t.events),
                {},
                {
                  style: t.style,
                  role: t.role,
                  shapeRendering: t.shapeRendering,
                  cx: t.x,
                  cy: t.y,
                  r: t.height,
                  className: t.className,
                },
              ),
            )
          : a.cloneElement(
              t.rectComponent,
              M(
                M({}, t.events),
                {},
                {
                  style: t.style,
                  role: t.role,
                  shapeRendering: t.shapeRendering,
                  x: t.x,
                  y: t.y,
                  rx: t.rx,
                  ry: t.ry,
                  width: t.width,
                  height: t.height,
                  className: t.className,
                },
              ),
            );
      };
      (_.propTypes = M(
        M({}, w.l.primitiveProps),
        {},
        {
          circleComponent: y().element,
          height: y().number,
          rectComponent: y().element,
          rx: y().number,
          ry: y().number,
          width: y().number,
          x: y().number,
          y: y().number,
        },
      )),
        (_.defaultProps = {
          circleComponent: a.createElement(P, null),
          rectComponent: a.createElement(S.U, null),
          role: "presentation",
          shapeRendering: "auto",
        });
      var L = n(17792),
        D = n(58853),
        I = n(68973),
        R = n(60344),
        N = n(4463),
        W = n(53841),
        F = n(83485),
        z = n(42017);
      function U(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function B(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? U(Object(n), !0).forEach(function (e) {
                q(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : U(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function q(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      var H = function (t) {
          var e = t.cx,
            n = t.cy,
            r = t.r,
            o = t.startAngle,
            a = t.endAngle,
            i = t.closedPath,
            c = Math.abs(a - o) / 2 + o,
            l = e + r * Math.cos(g.Ht(o)),
            u = n - r * Math.sin(g.Ht(o)),
            s = e + r * Math.cos(g.Ht(c)),
            f = n - r * Math.sin(g.Ht(c)),
            p = e + r * Math.cos(g.Ht(a)),
            d = n - r * Math.sin(g.Ht(a)),
            h = c - o <= 180 ? 0 : 1,
            v = a - c <= 180 ? 0 : 1,
            y = i
              ? " M ".concat(e, ", ").concat(n, " L ").concat(l, ", ").concat(u)
              : "M ".concat(l, ", ").concat(u),
            m = "A "
              .concat(r, ", ")
              .concat(r, ", 0, ")
              .concat(h, ", 0, ")
              .concat(s, ", ")
              .concat(f),
            b = "A "
              .concat(r, ", ")
              .concat(r, ", 0, ")
              .concat(v, ", 0, ")
              .concat(p, ", ")
              .concat(d),
            x = i ? "Z" : "";
          return "".concat(y, " ").concat(m, " ").concat(b, " ").concat(x);
        },
        V = function (t) {
          return (
            (t = (function (t) {
              var e = g.xs(t.ariaLabel, t),
                n = g.xs(t.desc, t),
                r = g.xs(t.id, t),
                o = g.F3(p()({ stroke: "black", fill: "none" }, t.style), t),
                a = g.xs(t.tabIndex, t);
              return p()({}, t, {
                ariaLabel: e,
                desc: n,
                id: r,
                style: o,
                tabIndex: a,
              });
            })(t)),
            a.cloneElement(
              t.pathComponent,
              B(
                B({}, t.events),
                {},
                {
                  "aria-label": t.ariaLabel,
                  d: H(t),
                  style: t.style,
                  desc: t.desc,
                  tabIndex: t.tabIndex,
                  className: t.className,
                  role: t.role,
                  shapeRendering: t.shapeRendering,
                  transform: t.transform,
                  clipPath: t.clipPath,
                },
              ),
            )
          );
        };
      (V.propTypes = B(
        B({}, w.l.primitiveProps),
        {},
        {
          closedPath: y().bool,
          cx: y().number,
          cy: y().number,
          datum: y().any,
          endAngle: y().number,
          pathComponent: y().element,
          r: y().number,
          startAngle: y().number,
        },
      )),
        (V.defaultProps = {
          pathComponent: a.createElement(z.y, null),
          role: "presentation",
          shapeRendering: "auto",
        });
      var $ = n(86225),
        Y = n(66339),
        Z = n.n(Y),
        K = n(20933),
        G = n(21222),
        X = function (t, e, n) {
          return "x" === n ? t * Math.cos(e) : -t * Math.sin(e);
        },
        Q = function (t) {
          var e = t.dependentAxis ? "radial" : "angular",
            n = "angular" === e ? "radial" : "angular";
          return t.horizontal ? n : e;
        },
        J = function (t, e) {
          return {
            tickStyle: g.F3(t.ticks, e),
            labelStyle: g.F3(t.tickLabels, e),
            gridStyle: g.F3(t.grid, e),
          };
        },
        tt = function (t) {
          var e = g.tQ(t),
            n = e.left,
            r = e.right,
            o = e.top,
            a = e.bottom,
            i = t.width,
            c = t.height;
          return Math.min(i - n - r, c - o - a) / 2;
        },
        et = function (t, e) {
          if (t.range && t.range[e]) return t.range[e];
          if (t.range && Array.isArray(t.range)) return t.range;
          if ("angular" === Q(t)) return [g.Ht(t.startAngle), g.Ht(t.endAngle)];
          var n = tt(t);
          return [t.innerRadius || 0, n];
        },
        nt = function (t) {
          var e = N.dd(t),
            n = K.q8(t, e),
            r = N.ge(t, e) || n.domain(),
            o = et(t, e);
          return n.range(o), n.domain(r), n;
        },
        rt = function (t, e) {
          if (t.disableInlineStyles) return {};
          var n = t.style || {};
          e = e || {};
          return {
            parent: h()({ height: "auto", width: "100%" }, n.parent, e.parent),
            axis: h()({}, n.axis, e.axis),
            axisLabel: h()({}, n.axisLabel, e.axisLabel),
            grid: h()({}, n.grid, e.grid),
            ticks: h()({}, n.ticks, e.ticks),
            tickLabels: h()({}, n.tickLabels, e.tickLabels),
          };
        },
        ot = function (t) {
          var e = t.axisAngle,
            n = t.startAngle,
            r = t.dependentAxis,
            o = N.dd(t),
            a = N.w5(t, o);
          return void 0 !== a && r ? g.vi(a) : void 0 === e ? n : e;
        },
        at = function (t, e, n, r) {
          var o = e.axisType,
            a = e.radius,
            i = e.scale,
            c = e.style,
            l = e.stringTicks,
            u = e.ticks,
            s = e.tickFormat,
            f = e.origin,
            p = s(n, r, u),
            d = l ? l[r] : n,
            h = J(c, {
              tick: d,
              tickValue: n,
              index: r,
              ticks: u,
              stringTicks: l,
              radius: a,
              scale: i,
              axisType: o,
              text: p,
            }).tickStyle,
            v = "radial" === o ? ot(t) : void 0,
            y = h.padding || h.size || 0,
            m = g.Ht(90 - v),
            b = "angular" === o ? i(n) : g.Ht(-1 * v),
            x = "angular" === o ? a : i(n);
          return "angular" === o
            ? {
                index: r,
                datum: d,
                style: h,
                x1: X(x, b, "x") + f.x,
                y1: X(x, b, "y") + f.y,
                x2: X(x + y, b, "x") + f.x,
                y2: X(x + y, b, "y") + f.y,
              }
            : {
                index: r,
                datum: d,
                style: h,
                x1: x * Math.cos(b) + Math.cos(m) * y + f.x,
                x2: x * Math.cos(b) - Math.cos(m) * y + f.x,
                y1: x * Math.sin(b) + Math.sin(m) * y + f.y,
                y2: x * Math.sin(b) - Math.sin(m) * y + f.y,
              };
        },
        it = function (t, e, n, r) {
          var o = e.axisType,
            a = e.radius,
            i = e.tickFormat,
            c = e.style,
            l = e.scale,
            u = e.ticks,
            s = e.stringTicks,
            f = e.origin,
            d = i(n, r, u),
            h = s ? s[r] : n,
            v = J(c, {
              text: d,
              tick: h,
              tickValue: n,
              index: r,
              ticks: u,
              stringTicks: s,
              radius: a,
              scale: l,
              axisType: o,
            }).labelStyle,
            y = t.tickLabelComponent,
            m =
              y.props && y.props.labelPlacement
                ? y.props.labelPlacement
                : t.labelPlacement,
            b = v.padding || 0,
            x = "radial" === o ? ot(t) : void 0,
            O = "angular" === o ? g.vi(l(n)) : x + 0,
            w =
              void 0 === v.angle
                ? G.Sw(p()({}, t, { labelPlacement: m }), O)
                : v.angle,
            C = "angular" === o ? a + b : l(n);
          return {
            index: r,
            datum: h,
            style: v,
            angle: w,
            textAnchor:
              v.textAnchor || G.Nf(p()({}, t, { labelPlacement: m }), O),
            text: d,
            x: C * Math.cos(g.Ht(O)) + f.x,
            y: -C * Math.sin(g.Ht(O)) + f.y,
          };
        },
        ct = function (t, e, n, r) {
          var o = e.axisType,
            a = e.radius,
            i = e.style,
            c = e.scale,
            l = e.stringTicks,
            u = e.ticks,
            s = e.tickFormat,
            f = e.origin,
            p = s(n, r, u),
            d = t.startAngle,
            h = t.endAngle,
            v = t.innerRadius,
            y = void 0 === v ? 0 : v,
            m = l ? l[r] : n,
            g = J(i, {
              tick: m,
              tickValue: n,
              index: r,
              ticks: u,
              stringTicks: l,
              radius: a,
              scale: c,
              axisType: o,
              text: p,
            }).gridStyle,
            b = c(n);
          return "angular" === o
            ? {
                index: r,
                datum: m,
                style: g,
                x1: X(a, b, "x") + f.x,
                y1: X(a, b, "y") + f.y,
                x2: X(y, b, "x") + f.x,
                y2: X(y, b, "y") + f.y,
              }
            : {
                style: g,
                index: r,
                datum: m,
                cx: f.x,
                cy: f.y,
                r: c(n),
                startAngle: d,
                endAngle: h,
              };
        },
        lt = function (t) {
          var e = (function (t) {
              var e = t.theme,
                n = void 0 === e ? {} : e,
                r = t.dependentAxis,
                o =
                  (n.polarAxis && n.polarAxis.style) ||
                  (n.axis && n.axis.style),
                a = r ? "polarDependentAxis" : "polarIndependentAxis",
                i = r ? "dependentAxis" : "independentAxis",
                c = (n[a] && n[a].style) || (n[i] && n[i].style);
              return o && c
                ? [
                    "axis",
                    "axisLabel",
                    "grid",
                    "parent",
                    "tickLabels",
                    "ticks",
                  ].reduce(function (t, e) {
                    return (t[e] = h()({}, c[e], o[e])), t;
                  }, {})
                : c || o;
            })((t = p()({ polar: !0 }, t))),
            n = rt(t, e),
            r = g.tQ(t),
            o = N.dd(t),
            a = Q(t),
            i = N.kM(t) ? t.tickValues : void 0,
            c = N.ge(t, o),
            l = et(t, o),
            u = nt(t),
            s = N.fj(t, u),
            f =
              "angular" === a
                ? (function (t, e) {
                    return Z()(t, function (t) {
                      return e(t) % (2 * Math.PI);
                    });
                  })(s, u)
                : s;
          return {
            axis: o,
            style: n,
            padding: r,
            stringTicks: i,
            axisType: a,
            scale: u,
            ticks: f,
            tickFormat: N.Js(t, u),
            domain: c,
            range: l,
            radius: tt(t),
            origin: g.IW(t),
          };
        },
        ut = function (t, e) {
          t = N.TY(t, e);
          var n = lt(t),
            r = n.style,
            o = n.scale,
            a = n.ticks,
            i = n.domain,
            c = t,
            l = c.width,
            u = c.height,
            s = c.standalone,
            f = c.theme,
            d = c.name,
            h = (function (t, e) {
              var n = e.style,
                r = e.axisType,
                o = e.radius,
                a = (e.scale, e.origin),
                i = t.startAngle,
                c = t.endAngle,
                l = t.innerRadius,
                u = void 0 === l ? 0 : l,
                s = "radial" === r ? g.Ht(ot(t)) : void 0;
              return "radial" === r
                ? {
                    style: n.axis,
                    x1: X(u, s, "x") + a.x,
                    x2: X(o, s, "x") + a.x,
                    y1: X(u, s, "y") + a.y,
                    y2: X(o, s, "y") + a.y,
                  }
                : {
                    style: n.axis,
                    cx: a.x,
                    cy: a.y,
                    r: o,
                    startAngle: i,
                    endAngle: c,
                  };
            })(t, n),
            v = (function (t, e) {
              var n = e.axisType,
                r = e.radius,
                o = e.style,
                a = (e.scale, e.origin),
                i = t.axisLabelComponent;
              if ("radial" !== n) return {};
              var c =
                  i.props && i.props.labelPlacement
                    ? i.props.labelPlacement
                    : t.labelPlacement,
                l = (o && o.axisLabel) || {},
                u = "radial" === n ? ot(t) : void 0,
                s =
                  void 0 === l.angle
                    ? G.Sw(p()({}, t, { labelPlacement: c }), u)
                    : l.angle,
                f = r + (l.padding || 0);
              return {
                style: l,
                angle: s,
                textAnchor:
                  l.textAnchor || G.Nf(p()({}, t, { labelPlacement: c }), u),
                verticalAnchor:
                  l.verticalAnchor ||
                  G.nV(p()({}, t, { labelPlacement: c }), u),
                text: t.label,
                x: X(f, g.Ht(u), "x") + a.x,
                y: X(f, g.Ht(u), "y") + a.y,
              };
            })(t, n),
            y = {
              parent: {
                style: r.parent,
                ticks: a,
                scale: o,
                width: l,
                height: u,
                domain: i,
                standalone: s,
                theme: f,
                name: d,
              },
            };
          return a.reduce(function (e, r, o) {
            return (
              (e[o] = {
                axis: h,
                axisLabel: v,
                ticks: at(t, n, r, o),
                tickLabels: it(t, n, r, o),
                grid: ct(t, n, r, o),
              }),
              e
            );
          }, y);
        };
      function st(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function ft(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? st(Object(n), !0).forEach(function (e) {
                pt(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : st(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function pt(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      function dt(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return ht(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return ht(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return ht(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function ht(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function vt(t, e) {
        for (var n = 0; n < e.length; n++) {
          var r = e[n];
          (r.enumerable = r.enumerable || !1),
            (r.configurable = !0),
            "value" in r && (r.writable = !0),
            Object.defineProperty(t, r.key, r);
        }
      }
      function yt(t, e) {
        return (
          (yt = Object.setPrototypeOf
            ? Object.setPrototypeOf.bind()
            : function (t, e) {
                return (t.__proto__ = e), t;
              }),
          yt(t, e)
        );
      }
      function mt(t) {
        var e = (function () {
          if ("undefined" === typeof Reflect || !Reflect.construct) return !1;
          if (Reflect.construct.sham) return !1;
          if ("function" === typeof Proxy) return !0;
          try {
            return (
              Boolean.prototype.valueOf.call(
                Reflect.construct(Boolean, [], function () {}),
              ),
              !0
            );
          } catch (t) {
            return !1;
          }
        })();
        return function () {
          var n,
            r = gt(t);
          if (e) {
            var o = gt(this).constructor;
            n = Reflect.construct(r, arguments, o);
          } else n = r.apply(this, arguments);
          return (function (t, e) {
            if (e && ("object" === typeof e || "function" === typeof e))
              return e;
            if (void 0 !== e)
              throw new TypeError(
                "Derived constructors may only return object or undefined",
              );
            return (function (t) {
              if (void 0 === t)
                throw new ReferenceError(
                  "this hasn't been initialised - super() hasn't been called",
                );
              return t;
            })(t);
          })(this, n);
        };
      }
      function gt(t) {
        return (
          (gt = Object.setPrototypeOf
            ? Object.getPrototypeOf.bind()
            : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t);
              }),
          gt(t)
        );
      }
      var bt = { width: 450, height: 300, padding: 50 },
        xt = (function (t) {
          !(function (t, e) {
            if ("function" !== typeof e && null !== e)
              throw new TypeError(
                "Super expression must either be null or a function",
              );
            (t.prototype = Object.create(e && e.prototype, {
              constructor: { value: t, writable: !0, configurable: !0 },
            })),
              Object.defineProperty(t, "prototype", { writable: !1 }),
              e && yt(t, e);
          })(i, t);
          var e,
            n,
            r,
            o = mt(i);
          function i() {
            return (
              (function (t, e) {
                if (!(t instanceof e))
                  throw new TypeError("Cannot call a class as a function");
              })(this, i),
              o.apply(this, arguments)
            );
          }
          return (
            (e = i),
            (n = [
              {
                key: "renderAxisLine",
                value: function (t) {
                  var e = t.dependentAxis
                      ? t.axisComponent
                      : t.circularAxisComponent,
                    n = this.getComponentProps(e, "axis", 0);
                  return a.cloneElement(e, n);
                },
              },
              {
                key: "renderLabel",
                value: function (t) {
                  var e = t.axisLabelComponent,
                    n = t.dependentAxis;
                  if (!t.label || !n) return null;
                  var r = this.getComponentProps(e, "axisLabel", 0);
                  return a.cloneElement(e, r);
                },
              },
              {
                key: "renderAxis",
                value: function (t) {
                  var e = this,
                    n = t.tickComponent,
                    r = t.tickLabelComponent,
                    o = t.name,
                    i = function (t) {
                      var e = t.style,
                        n = void 0 === e ? {} : e,
                        r = t.events,
                        o = void 0 === r ? {} : r;
                      return (
                        ("transparent" !== n.stroke &&
                          "none" !== n.stroke &&
                          0 !== n.strokeWidth) ||
                        !s()(o)
                      );
                    },
                    c =
                      "radial" === (t.dependentAxis ? "radial" : "angular")
                        ? t.circularGridComponent
                        : t.gridComponent,
                    l = this.dataKeys
                      .map(function (t, r) {
                        var c = p()(
                            { key: "".concat(o, "-tick-").concat(t) },
                            e.getComponentProps(n, "ticks", r),
                          ),
                          l = a.cloneElement(n, c);
                        return i(l.props) ? l : void 0;
                      })
                      .filter(Boolean),
                    u = this.dataKeys
                      .map(function (t, n) {
                        var r = p()(
                            { key: "".concat(o, "-grid-").concat(t) },
                            e.getComponentProps(c, "grid", n),
                          ),
                          l = a.cloneElement(c, r);
                        return i(l.props) ? l : void 0;
                      })
                      .filter(Boolean),
                    f = this.dataKeys.map(function (t, n) {
                      var i = p()(
                        { key: "".concat(o, "-tick-").concat(t) },
                        e.getComponentProps(r, "tickLabels", n),
                      );
                      return a.cloneElement(r, i);
                    }),
                    d = [this.renderAxisLine(t), this.renderLabel(t)].concat(
                      dt(l),
                      dt(u),
                      dt(f),
                    );
                  return this.renderGroup(t, d);
                },
              },
              {
                key: "renderGroup",
                value: function (t, e) {
                  var n = t.groupComponent;
                  return a.cloneElement(n, {}, e);
                },
              },
              {
                key: "shouldAnimate",
                value: function () {
                  return !!this.props.animate;
                },
              },
              {
                key: "render",
                value: function () {
                  var t = i.animationWhitelist,
                    e = N.TY(this.props, bt);
                  if (this.shouldAnimate()) return this.animateComponent(e, t);
                  var n = this.renderAxis(e);
                  return e.standalone
                    ? this.renderContainer(e.containerComponent, n)
                    : n;
                },
              },
            ]),
            n && vt(e.prototype, n),
            r && vt(e, r),
            Object.defineProperty(e, "prototype", { writable: !1 }),
            i
          );
        })(a.Component);
      (xt.animationWhitelist = [
        "style",
        "domain",
        "range",
        "tickCount",
        "tickValues",
        "padding",
        "width",
        "height",
      ]),
        (xt.displayName = "VictoryAxis"),
        (xt.role = "axis"),
        (xt.defaultTransitions = {
          onExit: { duration: 500 },
          onEnter: { duration: 500 },
        }),
        (xt.propTypes = ft(
          ft({}, w.l.baseProps),
          {},
          {
            axisAngle: y().number,
            axisComponent: y().element,
            axisLabelComponent: y().element,
            axisValue: y().oneOfType([y().number, y().string, y().object]),
            categories: y().oneOfType([
              y().arrayOf(y().string),
              y().shape({
                x: y().arrayOf(y().string),
                y: y().arrayOf(y().string),
              }),
            ]),
            circularAxisComponent: y().element,
            circularGridComponent: y().element,
            containerComponent: y().element,
            dependentAxis: y().bool,
            disableInlineStyles: y().bool,
            endAngle: y().number,
            events: y().arrayOf(
              y().shape({
                target: y().oneOf([
                  "axis",
                  "axisLabel",
                  "grid",
                  "ticks",
                  "tickLabels",
                ]),
                eventKey: y().oneOfType([
                  y().array,
                  C.BO([C._L, C.A7]),
                  y().string,
                ]),
                eventHandlers: y().object,
              }),
            ),
            gridComponent: y().element,
            innerRadius: C.A7,
            labelPlacement: y().oneOf([
              "parallel",
              "perpendicular",
              "vertical",
            ]),
            startAngle: y().number,
            stringMap: y().object,
            style: y().shape({
              parent: y().object,
              axis: y().object,
              axisLabel: y().object,
              grid: y().object,
              ticks: y().object,
              tickLabels: y().object,
            }),
            tickComponent: y().element,
            tickCount: C.BO([C._L, C.KO]),
            tickFormat: y().oneOfType([y().func, C.xx]),
            tickLabelComponent: y().element,
            tickValues: C.xx,
          },
        )),
        (xt.defaultProps = {
          axisComponent: a.createElement(W.c, null),
          axisLabelComponent: a.createElement(F.X, null),
          circularAxisComponent: a.createElement(V, null),
          circularGridComponent: a.createElement(V, null),
          containerComponent: a.createElement(L._, null),
          endAngle: 360,
          gridComponent: a.createElement(W.c, null),
          groupComponent: a.createElement("g", { role: "presentation" }),
          labelPlacement: "parallel",
          startAngle: 0,
          standalone: !0,
          theme: D.J.grayscale,
          tickComponent: a.createElement(W.c, null),
          tickLabelComponent: a.createElement(F.X, null),
        }),
        (xt.getDomain = N.ge),
        (xt.getAxis = N.dd),
        (xt.getScale = nt),
        (xt.getStyles = function (t) {
          return rt(t, bt.style);
        }),
        (xt.getBaseProps = function (t) {
          return ut(t, bt);
        }),
        (xt.expectedComponents = [
          "axisComponent",
          "circularAxisComponent",
          "groupComponent",
          "containerComponent",
          "tickComponent",
          "tickLabelComponent",
          "gridComponent",
          "circularGridComponent",
        ]);
      const Ot = (0, $.o)(xt, {
        components: [
          { name: "axis", index: 0 },
          { name: "axisLabel", index: 0 },
          { name: "grid" },
          { name: "parent", index: "parent" },
          { name: "ticks" },
          { name: "tickLabels" },
        ],
      });
      function wt(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return Ct(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return Ct(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return Ct(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function Ct(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      var St = { width: 450, height: 300, padding: 50 };
      function At(t, e) {
        var n = (function (t) {
            var e = t.style && t.style.parent;
            return {
              parent: h()({}, e, {
                height: "100%",
                width: "100%",
                userSelect: "none",
              }),
            };
          })(t),
          r = (t = g.TY(t, St, "chart")),
          o = r.horizontal,
          a = r.polar,
          i = x.Oz(t, e),
          c = x.CP(t, e, i),
          l = Et(t, e, i),
          u = {
            x: Pt(p()({}, t, { categories: c }), "x", e),
            y: Pt(p()({}, t, { categories: c }), "y", e),
          },
          s = { x: g.rx(t, "x"), y: g.rx(t, "y") },
          f = {
            x: K.j$(t, "x") || x.yZ(t, "x"),
            y: K.j$(t, "y") || x.yZ(t, "y"),
          };
        return {
          categories: c,
          domain: u,
          range: s,
          horizontal: o,
          scale: {
            x: f.x.domain(u.x).range(o ? s.y : s.x),
            y: f.y.domain(u.y).range(o ? s.x : s.y),
          },
          stringMap: l,
          style: n,
          origin: a ? g.IW(t) : N.P$(u),
          padding: g.tQ(t),
        };
      }
      function jt(t, e, n) {
        e = e || kt(t);
        var r = (n = n || At(t, e)).style.parent,
          o = t.height,
          i = t.polar,
          c = t.theme,
          l = t.width,
          u = n,
          s = u.origin,
          f = u.horizontal,
          p = t.name || "chart";
        return e.map(function (e, u) {
          var d = e.type && e.type.role,
            v = Array.isArray(e.props.style)
              ? e.props.style
              : h()({}, e.props.style, { parent: r }),
            y = (function (t, e, n) {
              var r = N.qM([t]);
              return r.length > 0
                ? (function (t, e, n) {
                    var r = n.domain,
                      o = n.scale,
                      a = n.stringMap,
                      i = n.categories;
                    return {
                      stringMap: a,
                      horizontal: n.horizontal,
                      categories: i,
                      startAngle: e.startAngle,
                      endAngle: e.endAngle,
                      innerRadius: e.innerRadius,
                      domain: r,
                      scale: o,
                    };
                  })(r[0], e, n)
                : {
                    categories: n.categories,
                    domain: n.domain,
                    range: n.range,
                    scale: n.scale,
                    stringMap: n.stringMap,
                    horizontal: n.horizontal,
                  };
            })(e, t, n),
            m = e.props.name || "".concat(p, "-").concat(d, "-").concat(u),
            g = h()(
              {
                horizontal: f,
                height: o,
                polar: i,
                theme: c,
                width: l,
                style: v,
                name: m,
                origin: i ? s : void 0,
                padding: n.padding,
                key: "".concat(m, "-key-").concat(u),
                standalone: !1,
              },
              y,
            );
          return a.cloneElement(e, g);
        });
      }
      var kt = function (t, e) {
          var n = a.Children.toArray(t.children),
            r = wt(n);
          if (0 === n.length) r.push(e.independent, e.dependent);
          else {
            var o = {
              dependent: N.X$(n, "dependent"),
              independent: N.X$(n, "independent"),
            };
            0 === o.dependent.length &&
              0 === o.independent.length &&
              (r = t.prependDefaultAxes
                ? [e.independent, e.dependent].concat(r)
                : r.concat([e.independent, e.dependent]));
          }
          return r;
        },
        Pt = function (t, e, n) {
          n = n || a.Children.toArray(t.children);
          var r = x.ge(t, e, n),
            o = N.OO(n, e);
          return o && o.props && o.props.invertAxis ? r.concat().reverse() : r;
        },
        Et = function (t, e, n) {
          return {
            x:
              n.x && 0 !== n.x.length
                ? n.x.reduce(function (t, e, n) {
                    return (t[e] = n + 1), t;
                  }, {})
                : null,
            y:
              n.y && 0 !== n.y.length
                ? n.y.reduce(function (t, e, n) {
                    return (t[e] = n + 1), t;
                  }, {})
                : null,
          };
        },
        Mt = n(50077),
        Tt = n.n(Mt);
      function _t(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function Lt(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? _t(Object(n), !0).forEach(function (e) {
                Dt(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : _t(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function Dt(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      var It = { width: 450, height: 300, padding: 50 },
        Rt = function (t) {
          var e = m.h(),
            n = e.getAnimationProps,
            r = e.setAnimationState,
            o = (0, e.getProps)(t),
            i = g.TY(o, It, "chart"),
            c = i.desc,
            l = i.eventKey,
            u = i.containerComponent,
            f = i.standalone,
            d = i.groupComponent,
            v = i.externalEventMutations,
            y = i.width,
            w = i.height,
            C = i.theme,
            S = i.polar,
            A = i.name,
            j = i.title,
            k = o.polar ? i.defaultPolarAxes : i.defaultAxes,
            P = a.useMemo(
              function () {
                return kt(i, k);
              },
              [i, k],
            ),
            E = a.useMemo(
              function () {
                return At(i, P);
              },
              [i, P],
            ),
            M = E.domain,
            T = E.scale,
            _ = E.style,
            L = E.origin,
            D = E.horizontal,
            R = a.useMemo(
              function () {
                var t = jt(o, P, E).map(function (t, e) {
                  var r = p()({ animate: n(o, t, e) }, t.props);
                  return a.cloneElement(t, r);
                });
                if (o.style && o.style.background) {
                  var e = (function (t, e) {
                    var n = t.backgroundComponent,
                      r = t.polar ? e.range.y[1] : e.range.y[0] - e.range.y[1],
                      o = e.range.x[1] - e.range.x[0],
                      i = t.horizontal
                        ? e.scale.y.range()[0]
                        : e.scale.x.range()[0],
                      c = t.horizontal
                        ? e.scale.x.range()[1]
                        : e.scale.y.range()[1],
                      l = t.polar ? e.origin.x : i,
                      u = t.polar ? e.origin.y : c,
                      s = t.name || "chart",
                      f = {
                        height: r,
                        polar: t.polar,
                        scale: e.scale,
                        style: t.style.background,
                        x: l,
                        y: u,
                        key: "".concat(s, "-background"),
                        width: o,
                      };
                    return a.cloneElement(n, h()({}, n.props, f));
                  })(o, E);
                  t.unshift(e);
                }
                return t;
              },
              [n, P, o, E],
            ),
            N = a.useMemo(
              function () {
                return f
                  ? {
                      desc: c,
                      domain: M,
                      width: y,
                      height: w,
                      horizontal: D,
                      name: A,
                      origin: S ? L : void 0,
                      polar: S,
                      theme: C,
                      title: j,
                      scale: T,
                      standalone: f,
                      style: _.parent,
                    }
                  : {};
              },
              [c, M, w, D, A, L, S, T, f, _, j, C, y],
            ),
            W = a.useMemo(
              function () {
                if (f) {
                  var e = h()({}, u.props, N, b.I(t));
                  return a.cloneElement(u, e);
                }
                return d;
              },
              [d, f, u, N, t],
            ),
            F = a.useMemo(
              function () {
                return x.IP(o);
              },
              [o],
            ),
            z = O.Y(t);
          return (
            a.useEffect(
              function () {
                return function () {
                  t.animate && r(z, t);
                };
              },
              [r, z, t],
            ),
            s()(F)
              ? a.cloneElement(W, W.props, R)
              : a.createElement(
                  I.Z,
                  {
                    container: W,
                    eventKey: l,
                    events: F,
                    externalEventMutations: v,
                  },
                  R,
                )
          );
        };
      (Rt.propTypes = Lt(
        Lt({}, w.l.baseProps),
        {},
        {
          backgroundComponent: y().element,
          children: y().oneOfType([y().arrayOf(y().node), y().node]),
          defaultAxes: y().shape({
            independent: y().element,
            dependent: y().element,
          }),
          defaultPolarAxes: y().shape({
            independent: y().element,
            dependent: y().element,
          }),
          endAngle: y().number,
          innerRadius: C.A7,
          prependDefaultAxes: y().bool,
          startAngle: y().number,
        },
      )),
        (Rt.defaultProps = {
          backgroundComponent: a.createElement(_, null),
          containerComponent: a.createElement(L._, null),
          defaultAxes: {
            independent: a.createElement(R.E, null),
            dependent: a.createElement(R.E, { dependentAxis: !0 }),
          },
          defaultPolarAxes: {
            independent: a.createElement(Ot, null),
            dependent: a.createElement(Ot, { dependentAxis: !0 }),
          },
          groupComponent: a.createElement("g", null),
          standalone: !0,
          theme: D.J.grayscale,
        });
      var Nt = a.memo(Rt, Tt());
      (Nt.displayName = "VictoryChart"),
        (Nt.expectedComponents = ["groupComponent", "containerComponent"]);
      var Wt = n(50235),
        Ft = n(42854),
        zt = n.n(Ft),
        Ut = n(66222),
        Bt = n.n(Ut),
        qt = n(87151),
        Ht = n.n(qt),
        Vt = n(12742),
        $t = n.n(Vt),
        Yt = n(98444),
        Zt = n.n(Yt),
        Kt = n(30637),
        Gt = n(62795);
      function Xt(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return Qt(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return Qt(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return Qt(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function Qt(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function Jt(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function te(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? Jt(Object(n), !0).forEach(function (e) {
                ee(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : Jt(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function ee(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      var ne = function (t) {
          var e = t.colorScale;
          return "string" === typeof e ? Kt.p(e) : e || [];
        },
        re = function (t) {
          var e = t.data,
            n = t.style;
          return e.map(function (t, r) {
            var o = h()({}, t.labels, n.labels);
            return g.F3(o, { datum: t, index: r, data: e });
          });
        },
        oe = function (t) {
          var e = t.orientation,
            n = t.theme,
            r = (function (t, e) {
              var n = t.style || {};
              return (
                (e = e || {}),
                {
                  parent: h()(n.parent, e.parent, {
                    height: "100%",
                    width: "100%",
                  }),
                  data: h()({}, n.data, e.data),
                  labels: h()({}, n.labels, e.labels),
                  border: h()({}, n.border, e.border),
                  title: h()({}, n.title, e.title),
                }
              );
            })(t, n && n.legend && n.legend.style ? n.legend.style : {}),
            o = ne(t),
            a = "horizontal" === e,
            i = g.tQ({ padding: t.borderPadding });
          return p()({}, t, {
            style: r,
            isHorizontal: a,
            colorScale: o,
            borderPadding: i,
          });
        },
        ae = function (t, e) {
          var n = t.itemsPerRow,
            r = t.isHorizontal;
          return n ? (r ? e % n : Math.floor(e / n)) : r ? e : 0;
        },
        ie = function (t, e) {
          var n = t.itemsPerRow,
            r = t.isHorizontal;
          return n ? (r ? Math.floor(e / n) : e % n) : r ? 0 : e;
        },
        ce = function (t) {
          var e = t.data,
            n = (t.style && t.style.data) || {},
            r = re(t);
          return e.map(function (e, o) {
            var a = e.symbol || {},
              i = r[o].fontSize,
              c = a.size || n.size || i / 2.5,
              l = t.symbolSpacer || Math.max(c, i);
            return te(
              te({}, e),
              {},
              {
                size: c,
                symbolSpacer: l,
                fontSize: i,
                textSize: Gt.Z9(e.name, r[o]),
                column: ae(t, o),
                row: ie(t, o),
              },
            );
          });
        },
        le = function (t, e) {
          var n = t.gutter || {},
            r = "object" === typeof n ? (n.left || 0) + (n.right || 0) : n || 0,
            o = Zt()(e, "column");
          return $t()(o).reduce(function (t, e, n) {
            var a = o[e].map(function (t) {
              return t.textSize.width + t.size + t.symbolSpacer + r;
            });
            return (t[n] = Math.max.apply(Math, Xt(a))), t;
          }, []);
        },
        ue = function (t, e) {
          var n = t.rowGutter || {},
            r = "object" === typeof n ? (n.top || 0) + (n.bottom || 0) : n || 0,
            o = Zt()(e, "row");
          return $t()(o).reduce(function (t, e, n) {
            var a = o[e].map(function (t) {
              return t.textSize.height + t.symbolSpacer + r;
            });
            return (t[n] = Math.max.apply(Math, Xt(a))), t;
          }, []);
        },
        se = function (t) {
          var e = (t.style && t.style.title) || {},
            n = Gt.Z9(t.title, e),
            r = e.padding || 0;
          return { height: n.height + 2 * r || 0, width: n.width + 2 * r || 0 };
        },
        fe = function (t, e) {
          var n = t.title,
            r = t.titleOrientation,
            o = t.centerTitle,
            a = t.borderPadding,
            i = e.height,
            c = e.width,
            l = (function (t) {
              var e = t.titleOrientation,
                n = t.centerTitle,
                r = t.titleComponent,
                o = (t.style && t.style.title) || {},
                a = (r.props && r.props.style) || {},
                i = (function (t, e) {
                  var n = {
                    textAnchor: "right" === t ? "end" : "start",
                    verticalAnchor: "bottom" === t ? "end" : "start",
                  };
                  if (e) {
                    var r = "top" === t || "bottom" === t;
                    return {
                      textAnchor: r ? "middle" : n.textAnchor,
                      verticalAnchor: r ? n.verticalAnchor : "middle",
                    };
                  }
                  return n;
                })(e, n);
              return Array.isArray(a)
                ? a.map(function (t) {
                    return h()({}, t, o, i);
                  })
                : h()({}, a, o, i);
            })(t),
            u = Array.isArray(l) ? l[0].padding : l.padding,
            s = "top" === r || "bottom" === r,
            f = "right" === r ? "right" : "left",
            p = {
              x: o ? c / 2 : a["bottom" === r ? "bottom" : "top"] + (u || 0),
              y: o ? i / 2 : a[f] + (u || 0),
            },
            d = function () {
              return a[r] + (u || 0);
            },
            v = s ? p.x : d(),
            y = s ? d() : p.y;
          return {
            x: "right" === r ? t.x + c - v : t.x + v,
            y: "bottom" === r ? t.y + i - y : t.y + y,
            style: l,
            text: n,
          };
        },
        pe = function (t, e) {
          var n = g.TY(t, e, "legend"),
            r = (t = p()({}, n, oe(n))),
            o = r.title,
            a = r.titleOrientation,
            i = ce(t),
            c = le(t, i),
            l = ue(t, i),
            u = o ? se(t) : { height: 0, width: 0 };
          return {
            height:
              "left" === a || "right" === a
                ? Math.max(Ht()(l), u.height)
                : Ht()(l) + u.height,
            width:
              "left" === a || "right" === a
                ? Ht()(c) + u.width
                : Math.max(Ht()(c), u.width),
          };
        },
        de = function (t, e) {
          var n = g.TY(t, e, "legend"),
            r = (t = p()({}, n, oe(n))),
            o = r.data,
            a = r.standalone,
            i = r.theme,
            c = r.padding,
            l = r.style,
            u = r.colorScale,
            s = r.gutter,
            f = r.rowGutter,
            d = r.borderPadding,
            v = r.title,
            y = r.titleOrientation,
            m = r.name,
            b = r.x,
            x = void 0 === b ? 0 : b,
            O = r.y,
            w = void 0 === O ? 0 : O,
            C = ce(t),
            S = le(t, C),
            A = ue(t, C),
            j = re(t),
            k = v ? se(t) : { height: 0, width: 0 },
            P = "left" === y ? k.width : 0,
            E = "top" === y ? k.height : 0,
            M = (s && "object" === typeof s && s.left) || 0,
            T = (f && "object" === typeof f && f.top) || 0,
            _ = pe(t, e),
            L = (function (t, e, n) {
              var r = t.x,
                o = t.y,
                a = t.borderPadding,
                i = t.style;
              return {
                x: r,
                y: o,
                height: (e || 0) + a.top + a.bottom,
                width: (n || 0) + a.left + a.right,
                style: p()({ fill: "none" }, i.border),
              };
            })(t, _.height, _.width),
            D = fe(t, L),
            I = {
              parent: {
                data: o,
                standalone: a,
                theme: i,
                padding: c,
                name: m,
                height: t.height,
                width: t.width,
                style: l.parent,
              },
              all: { border: L, title: D },
            };
          return C.reduce(function (t, e, n) {
            var r = u[n % u.length],
              a = h()({}, e.symbol, l.data, { fill: r }),
              i = zt()(e.eventKey) ? n : e.eventKey,
              c = (function (t, e, n) {
                var r = t.column,
                  o = t.row;
                return {
                  x: Bt()(r).reduce(function (t, e) {
                    return t + n[e];
                  }, 0),
                  y: Bt()(o).reduce(function (t, n) {
                    return t + e[n];
                  }, 0),
                };
              })(e, A, S),
              s = w + d.top + e.symbolSpacer,
              f = x + d.left + e.symbolSpacer,
              p = {
                index: n,
                data: o,
                datum: e,
                symbol: a.type || a.symbol || "circle",
                size: e.size,
                style: a,
                y: s + c.y + E + T,
                x: f + c.x + P + M,
              },
              v = {
                datum: e,
                data: o,
                text: e.name,
                style: j[n],
                y: p.y,
                x: p.x + e.symbolSpacer + e.size / 2,
              };
            return (t[i] = { data: p, labels: v }), t;
          }, I);
        };
      function he(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function ve(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? he(Object(n), !0).forEach(function (e) {
                ye(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : he(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function ye(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      var me = function (t) {
        return (
          (t = (function (t) {
            var e = g.xs(t.ariaLabel, t),
              n = g.xs(t.desc, t),
              r = g.xs(t.id, t),
              o = g.F3(p()({ fill: "none" }, t.style), t),
              a = g.xs(t.tabIndex, t);
            return p()({}, t, {
              ariaLabel: e,
              desc: n,
              id: r,
              style: o,
              tabIndex: a,
            });
          })(t)),
          a.cloneElement(
            t.rectComponent,
            ve(
              ve({}, t.events),
              {},
              {
                "aria-label": t.ariaLabel,
                style: t.style,
                desc: t.desc,
                tabIndex: t.tabIndex,
                transform: t.transform,
                className: t.className,
                role: t.role,
                shapeRendering: t.shapeRendering,
                x: t.x,
                y: t.y,
                width: t.width,
                height: t.height,
                clipPath: t.clipPath,
              },
            ),
          )
        );
      };
      function ge(t, e, n) {
        return "M "
          .concat(t, ", ")
          .concat(e, "\n      m ")
          .concat(-n, ", 0\n      a ")
          .concat(n, ", ")
          .concat(n, " 0 1,0 ")
          .concat(2 * n, ",0\n      a ")
          .concat(n, ", ")
          .concat(n, " 0 1,0 ")
          .concat(2 * -n, ",0");
      }
      function be(t, e, n) {
        var r = 0.87 * n,
          o = t - r,
          a = e + r,
          i = t + r - o;
        return "M "
          .concat(o, ", ")
          .concat(a, "\n      h")
          .concat(i, "\n      v-")
          .concat(i, "\n      h-")
          .concat(i, "\n      z");
      }
      function xe(t, e, n) {
        var r = 0.87 * n,
          o = Math.sqrt(r * r * 2);
        return "M "
          .concat(t, ", ")
          .concat(e + o, "\n      l ")
          .concat(o, ", -")
          .concat(o, "\n      l -")
          .concat(o, ", -")
          .concat(o, "\n      l -")
          .concat(o, ", ")
          .concat(o, "\n      l ")
          .concat(o, ", ")
          .concat(o, "\n      z");
      }
      function Oe(t, e, n) {
        var r = t + n,
          o = e - n,
          a = e + (n / 2) * Math.sqrt(3);
        return "M "
          .concat(t - n, ", ")
          .concat(o, "\n      L ")
          .concat(r, ", ")
          .concat(o, "\n      L ")
          .concat(t, ", ")
          .concat(a, "\n      z");
      }
      function we(t, e, n) {
        var r = t + n,
          o = e - (n / 2) * Math.sqrt(3),
          a = e + n;
        return "M "
          .concat(t - n, ", ")
          .concat(a, "\n      L ")
          .concat(r, ", ")
          .concat(a, "\n      L ")
          .concat(t, ", ")
          .concat(o, "\n      z");
      }
      function Ce(t, e, n) {
        var r = 1.1 * n,
          o = r / 1.5;
        return "\n      M "
          .concat(t - o / 2, ", ")
          .concat(e + r, "\n      v-")
          .concat(o, "\n      h-")
          .concat(o, "\n      v-")
          .concat(o, "\n      h")
          .concat(o, "\n      v-")
          .concat(o, "\n      h")
          .concat(o, "\n      v")
          .concat(o, "\n      h")
          .concat(o, "\n      v")
          .concat(o, "\n      h-")
          .concat(o, "\n      v")
          .concat(o, "\n      z");
      }
      function Se(t, e, n) {
        var r = 0.8 * n,
          o = r / 1.5;
        return "\n      M "
          .concat(t - o / 2, ", ")
          .concat(e + r + o, "\n      v-")
          .concat(2 * o, "\n      h-")
          .concat(o, "\n      v-")
          .concat(o, "\n      h")
          .concat(o, "\n      v-")
          .concat(o, "\n      h")
          .concat(o, "\n      v")
          .concat(o, "\n      h")
          .concat(o, "\n      v")
          .concat(o, "\n      h-")
          .concat(o, "\n      v")
          .concat(2 * o, "\n      z");
      }
      function Ae(t, e, n) {
        var r = 1.1 * n,
          o = r - 0.3 * r,
          a = t - r,
          i = e + o / 2,
          c = t + r - a;
        return "M "
          .concat(a, ", ")
          .concat(i, "\n      h")
          .concat(c, "\n      v-")
          .concat(o, "\n      h-")
          .concat(c, "\n      z");
      }
      function je(t, e, n) {
        var r = 1.35 * n,
          o = Math.PI / 5,
          a = Bt()(10).map(function (n) {
            var a = n % 2 === 0 ? r : r / 2;
            return ""
              .concat(a * Math.sin(o * (n + 1)) + t, ",\n        ")
              .concat(a * Math.cos(o * (n + 1)) + e);
          });
        return "M ".concat(a.join("L"), " z");
      }
      function ke(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function Pe(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? ke(Object(n), !0).forEach(function (e) {
                Ee(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : ke(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function Ee(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      (me.propTypes = ve(
        ve({}, w.l.primitiveProps),
        {},
        {
          height: y().number,
          rectComponent: y().element,
          width: y().number,
          x: y().number,
          y: y().number,
        },
      )),
        (me.defaultProps = {
          rectComponent: a.createElement(S.U, null),
          role: "presentation",
          shapeRendering: "auto",
        });
      var Me = function (t) {
          var e = t.x,
            n = t.y,
            o = t.size,
            a = t.symbol;
          if (t.getPath) return t.getPath(e, n, o);
          return ("function" === typeof r[a] ? r[a] : r.circle)(e, n, o);
        },
        Te = function (t) {
          t = (function (t) {
            var e = g.xs(t.ariaLabel, t),
              n = g.xs(t.desc, t),
              r = g.xs(t.id, t),
              o = g.xs(t.size, t),
              a = g.F3(t.style, t),
              i = g.xs(t.symbol, t),
              c = g.xs(t.tabIndex, t);
            return p()({}, t, {
              ariaLabel: e,
              desc: n,
              id: r,
              size: o,
              style: a,
              symbol: i,
              tabIndex: c,
            });
          })(t);
          var e = b.I(t);
          return a.cloneElement(
            t.pathComponent,
            Pe(
              Pe({}, t.events),
              {},
              {
                "aria-label": t.ariaLabel,
                d: Me(t),
                style: t.style,
                desc: t.desc,
                tabIndex: t.tabIndex,
                role: t.role,
                shapeRendering: t.shapeRendering,
                className: t.className,
                transform: t.transform,
                clipPath: t.clipPath,
              },
              e,
            ),
          );
        };
      function _e(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return Le(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return Le(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return Le(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function Le(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function De(t, e) {
        for (var n = 0; n < e.length; n++) {
          var r = e[n];
          (r.enumerable = r.enumerable || !1),
            (r.configurable = !0),
            "value" in r && (r.writable = !0),
            Object.defineProperty(t, r.key, r);
        }
      }
      function Ie(t, e) {
        return (
          (Ie = Object.setPrototypeOf
            ? Object.setPrototypeOf.bind()
            : function (t, e) {
                return (t.__proto__ = e), t;
              }),
          Ie(t, e)
        );
      }
      function Re(t) {
        var e = (function () {
          if ("undefined" === typeof Reflect || !Reflect.construct) return !1;
          if (Reflect.construct.sham) return !1;
          if ("function" === typeof Proxy) return !0;
          try {
            return (
              Boolean.prototype.valueOf.call(
                Reflect.construct(Boolean, [], function () {}),
              ),
              !0
            );
          } catch (t) {
            return !1;
          }
        })();
        return function () {
          var n,
            r = Ne(t);
          if (e) {
            var o = Ne(this).constructor;
            n = Reflect.construct(r, arguments, o);
          } else n = r.apply(this, arguments);
          return (function (t, e) {
            if (e && ("object" === typeof e || "function" === typeof e))
              return e;
            if (void 0 !== e)
              throw new TypeError(
                "Derived constructors may only return object or undefined",
              );
            return (function (t) {
              if (void 0 === t)
                throw new ReferenceError(
                  "this hasn't been initialised - super() hasn't been called",
                );
              return t;
            })(t);
          })(this, n);
        };
      }
      function Ne(t) {
        return (
          (Ne = Object.setPrototypeOf
            ? Object.getPrototypeOf.bind()
            : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t);
              }),
          Ne(t)
        );
      }
      (Te.propTypes = Pe(
        Pe({}, w.l.primitiveProps),
        {},
        {
          datum: y().object,
          getPath: y().func,
          pathComponent: y().element,
          size: y().oneOfType([y().number, y().func]),
          symbol: y().oneOfType([
            y().oneOf([
              "circle",
              "cross",
              "diamond",
              "plus",
              "minus",
              "square",
              "star",
              "triangleDown",
              "triangleUp",
            ]),
            y().func,
          ]),
          x: y().number,
          y: y().number,
        },
      )),
        (Te.defaultProps = {
          pathComponent: a.createElement(z.y, null),
          role: "presentation",
          shapeRendering: "auto",
        });
      var We = {
          orientation: "vertical",
          titleOrientation: "top",
          width: 450,
          height: 300,
          x: 0,
          y: 0,
        },
        Fe = (function (t) {
          !(function (t, e) {
            if ("function" !== typeof e && null !== e)
              throw new TypeError(
                "Super expression must either be null or a function",
              );
            (t.prototype = Object.create(e && e.prototype, {
              constructor: { value: t, writable: !0, configurable: !0 },
            })),
              Object.defineProperty(t, "prototype", { writable: !1 }),
              e && Ie(t, e);
          })(i, t);
          var e,
            n,
            r,
            o = Re(i);
          function i() {
            return (
              (function (t, e) {
                if (!(t instanceof e))
                  throw new TypeError("Cannot call a class as a function");
              })(this, i),
              o.apply(this, arguments)
            );
          }
          return (
            (e = i),
            (n = [
              {
                key: "renderChildren",
                value: function (t) {
                  var e = this,
                    n = t.dataComponent,
                    r = t.labelComponent,
                    o = t.title,
                    i = this.dataKeys
                      .map(function (t, r) {
                        if ("all" !== t) {
                          var o = e.getComponentProps(n, "data", r);
                          return a.cloneElement(n, o);
                        }
                      })
                      .filter(Boolean),
                    c = this.dataKeys
                      .map(function (t, n) {
                        if ("all" !== t) {
                          var o = e.getComponentProps(r, "labels", n);
                          return void 0 !== o.text && null !== o.text
                            ? a.cloneElement(r, o)
                            : void 0;
                        }
                      })
                      .filter(Boolean),
                    l = this.getComponentProps(
                      t.borderComponent,
                      "border",
                      "all",
                    ),
                    u = a.cloneElement(t.borderComponent, l);
                  if (o) {
                    var s = this.getComponentProps(t.title, "title", "all"),
                      f = a.cloneElement(t.titleComponent, s);
                    return [u].concat(_e(i), [f], _e(c));
                  }
                  return [u].concat(_e(i), _e(c));
                },
              },
              {
                key: "render",
                value: function () {
                  var t = this.constructor.role,
                    e = g.TY(this.props, We, t),
                    n = [this.renderChildren(e)];
                  return e.standalone
                    ? this.renderContainer(e.containerComponent, n)
                    : a.cloneElement(e.groupComponent, {}, n);
                },
              },
            ]) && De(e.prototype, n),
            r && De(e, r),
            Object.defineProperty(e, "prototype", { writable: !1 }),
            i
          );
        })(a.Component);
      (Fe.displayName = "VictoryLegend"),
        (Fe.role = "legend"),
        (Fe.propTypes = {
          borderComponent: y().element,
          borderPadding: y().oneOfType([
            y().number,
            y().shape({
              top: y().number,
              bottom: y().number,
              left: y().number,
              right: y().number,
            }),
          ]),
          centerTitle: y().bool,
          colorScale: y().oneOfType([
            y().arrayOf(y().string),
            y().oneOf([
              "grayscale",
              "qualitative",
              "heatmap",
              "warm",
              "cool",
              "red",
              "green",
              "blue",
            ]),
          ]),
          containerComponent: y().element,
          data: y().arrayOf(
            y().shape({
              name: y().string.isRequired,
              label: y().object,
              symbol: y().object,
            }),
          ),
          dataComponent: y().element,
          eventKey: y().oneOfType([y().func, C.BO([C._L, C.A7]), y().string]),
          events: y().arrayOf(
            y().shape({
              target: y().oneOf(["data", "labels", "parent"]),
              eventKey: y().oneOfType([
                y().array,
                C.BO([C._L, C.A7]),
                y().string,
              ]),
              eventHandlers: y().object,
            }),
          ),
          externalEventMutations: y().arrayOf(
            y().shape({
              callback: y().func,
              childName: y().oneOfType([y().string, y().array]),
              eventKey: y().oneOfType([
                y().array,
                C.BO([C._L, C.A7]),
                y().string,
              ]),
              mutation: y().func,
              target: y().oneOfType([y().string, y().array]),
            }),
          ),
          groupComponent: y().element,
          gutter: y().oneOfType([
            y().number,
            y().shape({ left: y().number, right: y().number }),
          ]),
          height: C.A7,
          itemsPerRow: C.A7,
          labelComponent: y().element,
          name: y().string,
          orientation: y().oneOf(["horizontal", "vertical"]),
          padding: y().oneOfType([
            y().number,
            y().shape({
              top: y().number,
              bottom: y().number,
              left: y().number,
              right: y().number,
            }),
          ]),
          rowGutter: y().oneOfType([
            y().number,
            y().shape({ top: y().number, bottom: y().number }),
          ]),
          sharedEvents: y().shape({
            events: y().array,
            getEventState: y().func,
          }),
          standalone: y().bool,
          style: y().shape({
            border: y().object,
            data: y().object,
            labels: y().object,
            parent: y().object,
            title: y().object,
          }),
          symbolSpacer: y().number,
          theme: y().object,
          title: y().oneOfType([y().string, y().array]),
          titleComponent: y().element,
          titleOrientation: y().oneOf(["top", "bottom", "left", "right"]),
          width: C.A7,
          x: C.A7,
          y: C.A7,
        }),
        (Fe.defaultProps = {
          borderComponent: a.createElement(me, null),
          data: [{ name: "Series 1" }, { name: "Series 2" }],
          containerComponent: a.createElement(L._, null),
          dataComponent: a.createElement(Te, null),
          groupComponent: a.createElement("g", null),
          labelComponent: a.createElement(F.X, null),
          standalone: !0,
          theme: D.J.grayscale,
          titleComponent: a.createElement(F.X, null),
        }),
        (Fe.getBaseProps = function (t) {
          return de(t, We);
        }),
        (Fe.getDimensions = function (t) {
          return pe(t, We);
        }),
        (Fe.expectedComponents = [
          "borderComponent",
          "containerComponent",
          "dataComponent",
          "groupComponent",
          "labelComponent",
          "titleComponent",
        ]);
      const ze = (0, $.o)(Fe);
      var Ue = n(77534);
      const Be = {
          circle: (t, e, n) =>
            "M "
              .concat(t, ", ")
              .concat(e, "\n      m ")
              .concat(-n, ", 0\n      a ")
              .concat(n, ", ")
              .concat(n, " 0 1,0 ")
              .concat(2 * n, ",0\n      a ")
              .concat(n, ", ")
              .concat(n, " 0 1,0 ")
              .concat(2 * -n, ",0"),
          dash: (t, e, n) => {
            const r = 1.1 * n,
              o = r - 0.3 * r,
              a = t - r,
              i = e + o / 2,
              c = 0.3 * (t + r - a),
              l = c / 3;
            return "M "
              .concat(a, ", ")
              .concat(i, "\n      h")
              .concat(c, "\n      v-")
              .concat(o, "\n      h-")
              .concat(c, "\n      z\n      M ")
              .concat(a + c + l, ", ")
              .concat(i, "\n      h")
              .concat(c, "\n      v-")
              .concat(o, "\n      h-")
              .concat(c, "\n      z\n      M ")
              .concat(a + 2 * c + 2 * l, ", ")
              .concat(i, "\n      h")
              .concat(c, "\n      v-")
              .concat(o, "\n      h-")
              .concat(c, "\n      z");
          },
          diamond: (t, e, n) => {
            const r = 0.87 * n,
              o = Math.sqrt(r * r * 2);
            return "M "
              .concat(t, ", ")
              .concat(e + o, "\n      l ")
              .concat(o, ", -")
              .concat(o, "\n      l -")
              .concat(o, ", -")
              .concat(o, "\n      l -")
              .concat(o, ", ")
              .concat(o, "\n      l ")
              .concat(o, ", ")
              .concat(o, "\n      z");
          },
          eyeSlash: (t, e, n) => {
            const r = e - 1.25 * n;
            return "m"
              .concat(t - 0.87 * n, ", ")
              .concat(r, " ")
              .concat(
                ".013 .013 0 0 2.179 2.219c.7-.204 1.418-.307 2.152-.307 2.859 0 5.464 1.551 7.814 4.654.243 .321.268 .753.073 1.097l-.073.111-.236.305c-.632.801-1.282 1.491-1.951 2.071l1.773 1.806c.382.389 .382 1.012 0 1.401l-.058.059c-.387.394-1.02.4-1.414.013l-.013-.013-11.732-11.956c-.382-.389-.382-1.012 0-1.401l.058-.059c.387-.394 1.02-.4 1.414-.013zm-.674 3.71 1.407 1.436c-.329.604-.516 1.298-.516 2.038 0 2.323 1.848 4.206 4.127 4.206.726 0 1.408-.191 2-.526l.966.984c-.956.396-1.945.593-2.966.593-2.859 0-5.464-1.551-7.814-4.654-.243-.321-.268-.753-.073-1.097l.073-.111.236-.305c.823-1.042 1.676-1.897 2.56-2.565zm2.177 2.22 4.072 4.149c-.377.167-.793.259-1.23.259-1.71 0-3.096-1.412-3.096-3.155 0-.445.091-.869.254-1.253zm2.842-2.953c-.43 0-.845.067-1.234.191l.865.882c.121-.015.244-.022.369-.022 1.71 0 3.096 1.412 3.096 3.155 0 .127-.007.252-.022.375l.866.882c.122-.397.187-.819.187-1.257 0-2.323-1.848-4.206-4.127-4.206z",
              );
          },
          minus: (t, e, n) => {
            const r = 1.1 * n,
              o = r - 0.3 * r,
              a = t - r,
              i = e + o / 2,
              c = t + r - a;
            return "M "
              .concat(a, ", ")
              .concat(i, "\n      h")
              .concat(c, "\n      v-")
              .concat(o, "\n      h-")
              .concat(c, "\n      z");
          },
          plus: (t, e, n) => {
            const r = 1.1 * n,
              o = r / 1.5;
            return "\n      M "
              .concat(t - o / 2, ", ")
              .concat(e + r, "\n      v-")
              .concat(o, "\n      h-")
              .concat(o, "\n      v-")
              .concat(o, "\n      h")
              .concat(o, "\n      v-")
              .concat(o, "\n      h")
              .concat(o, "\n      v")
              .concat(o, "\n      h")
              .concat(o, "\n      v")
              .concat(o, "\n      h-")
              .concat(o, "\n      v")
              .concat(o, "\n      z");
          },
          star: (t, e, n) => {
            const r = 1.35 * n,
              o = Math.PI / 5,
              a = [...Array(10).keys()].map((n) => {
                const a = n % 2 === 0 ? r : r / 2;
                return ""
                  .concat(a * Math.sin(o * (n + 1)) + t, ",\n        ")
                  .concat(a * Math.cos(o * (n + 1)) + e);
              });
            return "M ".concat(a.join("L"), " z");
          },
          square: (t, e, n) => {
            const r = 0.87 * n,
              o = t - r,
              a = e + r,
              i = t + r - o;
            return "M "
              .concat(o, ", ")
              .concat(a, "\n      h")
              .concat(i, "\n      v-")
              .concat(i, "\n      h-")
              .concat(i, "\n      z");
          },
          threshold: (t, e, n) => {
            const r = 1.1 * n,
              o = r - 0.3 * r,
              a = t - r,
              i = e + o / 2,
              c = 0.5 * (t + r - a),
              l = c / 3;
            return "M "
              .concat(a, ", ")
              .concat(i, "\n      h")
              .concat(c, "\n      v-")
              .concat(o, "\n      h-")
              .concat(c, "\n      z\n      M ")
              .concat(a + c + l, ", ")
              .concat(i, "\n      h")
              .concat(c, "\n      v-")
              .concat(o, "\n      h-")
              .concat(c, "\n      z");
          },
          triangleDown: (t, e, n) => {
            const r = t + n,
              o = e - n,
              a = e + (n / 2) * Math.sqrt(3);
            return "M "
              .concat(t - n, ", ")
              .concat(o, "\n      L ")
              .concat(r, ", ")
              .concat(o, "\n      L ")
              .concat(t, ", ")
              .concat(a, "\n      z");
          },
          triangleLeft: (t, e, n) => {
            const r = t - (n / 2) * Math.sqrt(3),
              o = t + n,
              a = e - n,
              i = e + n;
            return "M "
              .concat(o, ", ")
              .concat(a, "\n      L ")
              .concat(o, ", ")
              .concat(i, "\n      L ")
              .concat(r, ", ")
              .concat(e, "\n      z");
          },
          triangleRight: (t, e, n) => {
            const r = t - n,
              o = t + (n / 2) * Math.sqrt(3),
              a = e - n,
              i = e + n;
            return "M "
              .concat(r, ", ")
              .concat(a, "\n      L ")
              .concat(r, ", ")
              .concat(i, "\n      L ")
              .concat(o, ", ")
              .concat(e, "\n      z");
          },
          triangleUp: (t, e, n) => {
            const r = t + n,
              o = e - (n / 2) * Math.sqrt(3),
              a = e + n;
            return "M "
              .concat(t - n, ", ")
              .concat(a, "\n      L ")
              .concat(r, ", ")
              .concat(a, "\n      L ")
              .concat(t, ", ")
              .concat(o, "\n      z");
          },
        },
        qe = (t) => {
          const { x: e, y: n } = t,
            r = g.xs(t.size, t);
          if (t.getPath) return t.getPath(e, n, r);
          const o = {
              circle: Be.circle,
              square: Be.square,
              diamond: Be.diamond,
              eyeSlash: Be.eyeSlash,
              triangleDown: Be.triangleDown,
              triangleLeft: Be.triangleLeft,
              triangleRight: Be.triangleRight,
              triangleUp: Be.triangleUp,
              plus: Be.plus,
              minus: Be.minus,
              star: Be.star,
              dash: Be.dash,
              threshold: Be.threshold,
            },
            a = g.xs(t.symbol, t);
          return ("function" === typeof o[a] ? o[a] : o.square)(e, n, r);
        },
        He = (t) => {
          var {
              active: e,
              className: n,
              clipPath: r,
              datum: i,
              desc: c,
              events: l,
              pathComponent: u = a.createElement(z.y, null),
              role: s = "presentation",
              shapeRendering: f = "auto",
              tabIndex: p,
              transform: d,
            } = t,
            h = (0, o.__rest)(t, [
              "active",
              "className",
              "clipPath",
              "datum",
              "desc",
              "events",
              "pathComponent",
              "role",
              "shapeRendering",
              "tabIndex",
              "transform",
            ]);
          const v = Object.assign(
            {
              active: e,
              className: n,
              clipPath: r,
              datum: i,
              desc: c,
              events: l,
              role: s,
              shapeRendering: f,
              tabIndex: p,
              transform: d,
            },
            h,
          );
          return a.cloneElement(
            u,
            Object.assign(
              Object.assign(
                { className: n, clipPath: r, d: qe(v), desc: g.xs(c, v) },
                l,
              ),
              {
                role: s,
                shapeRendering: f,
                style: g.F3(h.style, v),
                tabIndex: g.xs(p, v),
                transform: d,
              },
            ),
          );
        };
      He.displayName = "ChartPoint";
      var Ve = n(79674);
      const $e = (t) => {
        var {
            colorScale: e,
            containerComponent: n = a.createElement(Wt.B, null),
            dataComponent: r = a.createElement(He, null),
            labelComponent: i = a.createElement(Ue.D, null),
            name: c,
            patternScale: l,
            responsive: u = !0,
            style: s,
            themeColor: f,
            titleComponent: p = a.createElement(Ue.D, null),
            theme: d = (0, Ve.gh)(f),
          } = t,
          h = (0, o.__rest)(t, [
            "colorScale",
            "containerComponent",
            "dataComponent",
            "labelComponent",
            "name",
            "patternScale",
            "responsive",
            "style",
            "themeColor",
            "titleComponent",
            "theme",
          ]);
        const v = a.cloneElement(
          n,
          Object.assign({ responsive: u, theme: d }, n.props),
        );
        return a.createElement(
          ze,
          Object.assign(
            {
              colorScale: e,
              containerComponent: v,
              dataComponent: r,
              labelComponent: a.cloneElement(
                i,
                Object.assign(
                  Object.assign(
                    {},
                    c && {
                      id: (t) =>
                        ""
                          .concat(c, "-")
                          .concat(i.type.displayName, "-")
                          .concat(t.index),
                    },
                  ),
                  i.props,
                ),
              ),
              name: c,
              style: (() => {
                if (!l) return s;
                const t = s ? Object.assign({}, s) : {};
                return (
                  (t.data = Object.assign(
                    {
                      fill: (t) => {
                        let { index: n } = t;
                        const r =
                            d && d.legend && d.legend.colorScale
                              ? d.legend.colorScale[
                                  n % d.legend.colorScale.length
                                ]
                              : void 0,
                          o = e ? e[n % e.length] : r,
                          a = l[n % l.length];
                        return a || o;
                      },
                    },
                    t.data,
                  )),
                  t
                );
              })(),
              theme: d,
              titleComponent: a.cloneElement(
                p,
                Object.assign(
                  Object.assign(
                    {},
                    c && {
                      id: () => "".concat(c, "-").concat(p.type.displayName),
                    },
                  ),
                  p.props,
                ),
              ),
            },
            h,
          ),
        );
      };
      ($e.displayName = "ChartLegend"),
        c()($e, ze, { getBaseProps: !0 }),
        ($e.getBaseProps = (t) => {
          const e = (0, Ve.gh)(null);
          return ze.getBaseProps(
            Object.assign({ titleComponent: a.createElement(Ue.D, null) }, t),
            {
              height: e.chart.height,
              orientation: e.legend.orientation,
              titleOrientation: e.legend.titleOrientation,
              x: 0,
              y: 0,
              width: e.chart.width,
            },
          );
        });
      var Ye = n(98278),
        Ze = n(70219);
      const Ke = (t) => {
          let { text: e, theme: n } = t;
          const r = n.legend.style.labels;
          return Gt.Z9(e, Object.assign({}, r));
        },
        Ge = (t) => {
          let { height: e, padding: n, width: r } = t;
          const { top: o, bottom: a, left: i, right: c } = g.tQ({ padding: n }),
            l = g.H5({ height: e, width: r, padding: n });
          return {
            x: l + i + (r - 2 * l - i - c) / 2,
            y: l + o + (e - 2 * l - o - a) / 2,
          };
        },
        Xe = (t) => {
          let {
            legendData: e,
            legendOrientation: n,
            legendProps: r,
            theme: o,
          } = t;
          return e || r.data
            ? ze.getDimensions(
                Object.assign({ data: e, orientation: n, theme: o }, r),
              )
            : {};
        },
        Qe = (t) => {
          let {
            dx: e = 0,
            height: n,
            legendPosition: r,
            legendData: o,
            legendOrientation: a,
            legendProps: i,
            padding: c,
            theme: l,
            width: u,
          } = t;
          const { left: s, right: f } = g.tQ({ padding: c }),
            p = u - s - f,
            d = Xe({
              legendData: o,
              legendOrientation: a,
              legendProps: i,
              theme: l,
            });
          let h = 0;
          switch (r) {
            case "bottom-left":
              h = s + e;
              break;
            case "right":
              h = p + Ye.cV.legend.margin + s + e;
              break;
            default:
              h = e;
          }
          return u - h > d.width;
        },
        Je = (t) => {
          let {
              dx: e,
              height: n,
              legendPosition: r,
              legendData: o,
              legendOrientation: a,
              legendProps: i,
              padding: c,
              theme: l,
              width: u,
            } = t,
            s = o ? o.length : 0;
          for (let f = s; f > 0; f--) {
            if (
              Qe({
                dx: e,
                height: n,
                legendPosition: r,
                legendData: o,
                legendOrientation: a,
                legendProps: Object.assign(Object.assign({}, i), {
                  itemsPerRow: f,
                }),
                padding: c,
                theme: l,
                width: u,
              })
            ) {
              s = f;
              break;
            }
          }
          return s;
        },
        tn = (t) => {
          var { chartType: e } = t,
            n = (0, o.__rest)(t, ["chartType"]);
          return "pie" === e ? an(n) : rn(n);
        },
        en = (t) => {
          var { chartType: e } = t,
            n = (0, o.__rest)(t, ["chartType"]);
          switch (e) {
            case "pie":
              return cn(n);
            case "bullet":
              return nn(n);
            default:
              return on(n);
          }
        },
        nn = (t) => {
          let {
            dy: e = 0,
            height: n,
            legendPosition: r,
            legendData: o,
            legendOrientation: a,
            legendProps: i,
            padding: c,
            theme: l,
            width: u,
          } = t;
          const { left: s, right: f } = g.tQ({ padding: c }),
            p = n;
          switch (r) {
            case "bottom":
            case "bottom-left":
              return p + Ye.cV.legend.margin + e;
            case "right": {
              const t = (t) => (t && t.length > 0 ? 17 : 0);
              return (
                (p -
                  Xe({
                    legendData: o,
                    legendOrientation: a,
                    legendProps: i,
                    theme: l,
                  }).height) /
                  2 +
                t(o)
              );
            }
            default:
              return e;
          }
        },
        rn = (t) => {
          let {
            dx: e = 0,
            height: n,
            legendData: r,
            legendOrientation: o,
            legendPosition: a,
            legendProps: i,
            padding: c,
            theme: l,
            width: u,
          } = t;
          const { top: s, bottom: f, left: p, right: d } = g.tQ({ padding: c }),
            h = (Math.abs(n - (f + s)), Math.abs(u - (p + d))),
            v = Xe({
              legendData: r,
              legendOrientation: o,
              legendProps: i,
              theme: l,
            });
          switch (a) {
            case "bottom":
              return u > v.width ? Math.round((u - v.width) / 2) + e : e;
            case "bottom-left":
              return p + e;
            case "right":
              return h + Ye.cV.legend.margin + p + e;
            default:
              return e;
          }
        },
        on = (t) => {
          let {
            dy: e = 0,
            height: n,
            legendPosition: r,
            legendData: o,
            legendOrientation: a,
            legendProps: i,
            padding: c,
            theme: l,
            width: u,
          } = t;
          const { top: s, bottom: f, left: p, right: d } = g.tQ({ padding: c }),
            h = Math.abs(n - (f + s));
          Math.abs(u - (p + d));
          switch (r) {
            case "bottom":
            case "bottom-left":
              return h + 2 * Ye.cV.legend.margin + s + e;
            case "right": {
              const t = (t) => (t && t.length > 0 ? 2 : 0);
              return (
                h / 2 +
                s -
                Xe({
                  legendData: o,
                  legendOrientation: a,
                  legendProps: i,
                  theme: l,
                }).height /
                  2 +
                t(o)
              );
            }
            default:
              return e;
          }
        },
        an = (t) => {
          let {
            dx: e = 0,
            height: n,
            legendData: r,
            legendOrientation: o,
            legendPosition: a,
            legendProps: i,
            padding: c,
            theme: l,
            width: u,
          } = t;
          const s = Ge({ height: n, padding: c, width: u }),
            f = g.H5({ height: n, width: u, padding: c }),
            p = Xe({
              legendData: r,
              legendOrientation: o,
              legendProps: i,
              theme: l,
            });
          switch (a) {
            case "bottom":
              return u > p.width ? Math.round((u - p.width) / 2) + e : e;
            case "right":
              return s.x + Ye.cV.label.margin + e + f;
            default:
              return e;
          }
        },
        cn = (t) => {
          let {
            dy: e = 0,
            height: n,
            legendPosition: r,
            legendData: o,
            legendOrientation: a,
            legendProps: i,
            padding: c,
            theme: l,
            width: u,
          } = t;
          const s = Ge({ height: n, padding: c, width: u }),
            f = g.H5({ height: n, width: u, padding: c });
          switch (r) {
            case "bottom":
              return s.y + Ye.cV.legend.margin + f + e;
            case "right": {
              const t = Xe({
                  legendData: o,
                  legendOrientation: a,
                  legendProps: i,
                  theme: l,
                }),
                e = (t) => (t && t.length > 0 ? 2 : 0);
              return s.y - t.height / 2 + e(o);
            }
            default:
              return e;
          }
        },
        ln = (t, e, n) =>
          "number" == typeof e
            ? e
            : "object" == typeof e && Object.keys(e).length > 0
              ? e[t] || 0
              : ln(t, n, 0);
      var un = n(10859),
        sn = n(7953);
      const fn = (t) => {
        var {
            ariaDesc: e,
            ariaTitle: n,
            children: r,
            colorScale: i,
            hasPatterns: c,
            legendAllowWrap: u = !1,
            legendComponent: s = a.createElement($e, null),
            legendData: f,
            legendPosition: p = Ye.cV.legend.position,
            legendDirection: d = "ltr",
            name: v,
            padding: y,
            patternScale: m,
            showAxis: g = !0,
            themeColor: b,
            theme: x = (0, sn.EH)(b, g),
            containerComponent: O = a.createElement(Wt.B, null),
            legendOrientation: w = x.legend.orientation,
            height: C = x.chart.height,
            width: S = x.chart.width,
          } = t,
          A = (0, o.__rest)(t, [
            "ariaDesc",
            "ariaTitle",
            "children",
            "colorScale",
            "hasPatterns",
            "legendAllowWrap",
            "legendComponent",
            "legendData",
            "legendPosition",
            "legendDirection",
            "name",
            "padding",
            "patternScale",
            "showAxis",
            "themeColor",
            "theme",
            "containerComponent",
            "legendOrientation",
            "height",
            "width",
          ]);
        const j = {
            bottom: ln("bottom", y, x.chart.padding),
            left: ln("left", y, x.chart.padding),
            right: ln("right", y, x.chart.padding),
            top: ln("top", y, x.chart.padding),
          },
          {
            defaultColorScale: k,
            defaultPatternScale: P,
            isPatternDefs: E,
            patternId: M,
          } = (0, un.cA)({
            colorScale: i,
            patternScale: m,
            hasPatterns: c,
            themeColorScale: x.chart.colorScale,
          });
        let T;
        O.props.labelComponent &&
          "ChartLegendTooltip" === O.props.labelComponent.type.displayName &&
          (T = a.cloneElement(
            O.props.labelComponent,
            Object.assign(
              Object.assign({ theme: x }, P && { patternScale: P }),
              O.props.labelComponent.props,
            ),
          ));
        const _ = a.cloneElement(
          O,
          Object.assign(
            Object.assign(
              Object.assign({ desc: e, title: n, theme: x }, O.props),
              { className: (0, Ze.g)({ className: O.props.className }) },
            ),
            T && { labelComponent: T },
          ),
        );
        let L = 0;
        "rtl" === d &&
          (L = ((t, e) => {
            let n = 0;
            return (
              t.map((t) => {
                const r = Ke({ text: t.name, theme: e }).width;
                r > n && (n = r);
              }),
              n
            );
          })(f, x));
        const D = a.cloneElement(
            s,
            Object.assign(
              Object.assign(
                Object.assign(
                  Object.assign(
                    Object.assign(
                      { data: f },
                      v && {
                        name: "".concat(v, "-").concat(s.type.displayName),
                      },
                    ),
                    { orientation: w, theme: x },
                  ),
                  "rtl" === d && {
                    dataComponent: s.props.dataComponent
                      ? a.cloneElement(s.props.dataComponent, {
                          transform: "translate(".concat(L, ")"),
                        })
                      : a.createElement(He, {
                          transform: "translate(".concat(L, ")"),
                        }),
                  },
                ),
                "rtl" === d && {
                  labelComponent: s.props.labelComponent
                    ? a.cloneElement(s.props.labelComponent, {
                        direction: "rtl",
                        dx: L - 30,
                      })
                    : a.createElement(Ue.D, { direction: "rtl", dx: L - 30 }),
                },
              ),
              s.props,
            ),
          ),
          I = (() => {
            if (!D.props.data) return null;
            let t = 0,
              e = 0,
              n = 0,
              o = D.props.title ? 10 : 0;
            return (
              a.Children.toArray(r).map((t) => {
                "axis" === t.type.role &&
                  t.props.label &&
                  !t.props.dependentAxis &&
                  ((n = Ke({ text: t.props.label, theme: x }).height + 10),
                  (o = 0));
              }),
              "bottom" === p
                ? (e += n + o)
                : "bottom-left" === p && ((e += n + o), (t = -10)),
              g || (e -= l.Z.value),
              ((t) => {
                let {
                  allowWrap: e = !0,
                  chartType: n = "chart",
                  colorScale: r,
                  dx: o = 0,
                  dy: i = 0,
                  height: c,
                  legendComponent: l,
                  padding: u,
                  patternScale: s,
                  position: f = Ye.cV.legend.position,
                  theme: p,
                  width: d,
                  orientation: v = p.legend.orientation,
                } = t;
                const y = l.props ? l.props : {},
                  m = e
                    ? Je({
                        dx: o,
                        height: c,
                        legendData: y.data,
                        legendOrientation: y.legendOrientation
                          ? y.legendOrientation
                          : v,
                        legendPosition: f,
                        legendProps: y,
                        padding: u,
                        theme: p,
                        width: d,
                      })
                    : void 0,
                  g = h()({}, l.props, { itemsPerRow: m }),
                  b = tn({
                    chartType: n,
                    dx: o,
                    height: c,
                    legendData: g.data,
                    legendOrientation: g.legendOrientation
                      ? g.legendOrientation
                      : v,
                    legendPosition: f,
                    legendProps: g,
                    padding: u,
                    theme: p,
                    width: d,
                  }),
                  x = en({
                    chartType: n,
                    dy: i,
                    height: c,
                    legendData: g.data,
                    legendOrientation: g.legendOrientation
                      ? g.legendOrientation
                      : v,
                    legendProps: g,
                    legendPosition: f,
                    padding: u,
                    theme: p,
                    width: d,
                  }),
                  O = h()({}, l.props, {
                    colorScale: r,
                    itemsPerRow: m,
                    orientation: v,
                    patternScale: s,
                    standalone: !1,
                    theme: p,
                    x: b > 0 ? b : 0,
                    y: x > 0 ? x : 0,
                  });
                return a.cloneElement(l, O);
              })(
                Object.assign(
                  {
                    allowWrap: !0 === u || "function" === typeof u,
                    chartType: "chart",
                    colorScale: i,
                    dx: t,
                    dy: e,
                    height: C,
                    legendComponent: D,
                    padding: j,
                    position: p,
                    theme: x,
                    width: S,
                  },
                  P && { patternScale: P },
                ),
              )
            );
          })();
        return (
          (0, a.useEffect)(() => {
            if ("function" === typeof u) {
              const t = ((t) => {
                let {
                  legendData: e,
                  legendOrientation: n,
                  legendProps: r,
                  theme: o,
                } = t;
                const a = Xe({
                    legendData: e,
                    legendOrientation: n,
                    legendProps: r,
                    theme: o,
                  }),
                  i = Xe({
                    legendData: e,
                    legendOrientation: n,
                    legendProps: Object.assign(Object.assign({}, r), {
                      itemsPerRow: void 0,
                    }),
                    theme: o,
                  });
                return Math.abs(a.height - i.height);
              })({
                legendData: I.props.data,
                legendOrientation: I.props.orientation,
                legendProps: I.props,
                theme: x,
              });
              u(t);
            }
          }, [I, u, x, S]),
          a.createElement(
            Nt,
            Object.assign(
              {
                colorScale: i,
                containerComponent: _,
                height: C,
                name: v,
                padding: j,
                theme: x,
                width: S,
              },
              A,
            ),
            a.Children.toArray(r).map((t, e) => {
              if (a.isValidElement(t)) {
                const n = (0, o.__rest)(t.props, []);
                return a.cloneElement(
                  t,
                  Object.assign(
                    Object.assign(
                      Object.assign(
                        Object.assign(
                          Object.assign(
                            { colorScale: i },
                            P && { patternScale: P },
                          ),
                          v &&
                            void 0 !== typeof t.name && {
                              name: ""
                                .concat(v, "-")
                                .concat(t.type.displayName, "-")
                                .concat(e),
                            },
                        ),
                        { theme: x },
                      ),
                      n,
                    ),
                    "ChartPie" === t.type.displayName && {
                      data: (0, un.xA)(n.data, P),
                    },
                  ),
                );
              }
              return t;
            }),
            I,
            E && (0, un.LF)({ patternId: M, colorScale: k }),
          )
        );
      };
      (fn.displayName = "Chart"), c()(fn, Nt);
    },
    4464: (t, e, n) => {
      "use strict";
      n.d(e, { C: () => p });
      var r = n(75971),
        o = n(72791),
        a = n(62110),
        i = n.n(a),
        c = n(60344),
        l = n(50235),
        u = n(77534),
        s = n(79674),
        f = n(7953);
      const p = (t) => {
        var {
            axisLabelComponent: e = o.createElement(u.D, null),
            containerComponent: n = o.createElement(l.B, null),
            name: a,
            showGrid: i = !1,
            themeColor: p,
            tickLabelComponent: d = o.createElement(u.D, null),
            theme: h = (0, s.gh)(p),
          } = t,
          v = (0, r.__rest)(t, [
            "axisLabelComponent",
            "containerComponent",
            "name",
            "showGrid",
            "themeColor",
            "tickLabelComponent",
            "theme",
          ]);
        const y = o.cloneElement(n, Object.assign({ theme: h }, n.props));
        return o.createElement(
          c.E,
          Object.assign(
            {
              axisLabelComponent: o.cloneElement(
                e,
                Object.assign(
                  Object.assign(
                    {},
                    a && {
                      id: () => "".concat(a, "-").concat(e.type.displayName),
                    },
                  ),
                  e.props,
                ),
              ),
              containerComponent: y,
              name: a,
              theme: i ? (0, f.zU)(p) : h,
              tickLabelComponent: o.cloneElement(
                d,
                Object.assign(
                  Object.assign(
                    {},
                    a && {
                      id: (t) =>
                        ""
                          .concat(a, "-")
                          .concat(d.type.displayName, "-")
                          .concat(t.index),
                    },
                  ),
                  d.props,
                ),
              ),
            },
            v,
          ),
        );
      };
      (p.displayName = "ChartAxis"), i()(p, c.E);
    },
    5291: (t, e, n) => {
      "use strict";
      n.d(e, { B: () => Gt });
      var r = n(75971),
        o = n(72791),
        a = n(62110),
        i = n.n(a),
        c = n(52007),
        l = n.n(c),
        u = n(42854),
        s = n.n(u),
        f = n(15687),
        p = n.n(f),
        d = n(20933),
        h = n(15896),
        v = n(8091),
        y = n(28275),
        m = n(54481),
        g = n(21222),
        b = function (t, e) {
          var n = v.TY(t, e, "bar");
          t = p()(
            {},
            n,
            (function (t) {
              var e = t.polar,
                n = v.Lo(t, "bar"),
                r = t.disableInlineStyles ? {} : v.Wi(t.style, n),
                o = t.range || { x: v.rx(t, "x"), y: v.rx(t, "y") },
                a = { x: y.x1(t, "x"), y: y.x1(t, "y") },
                i = {
                  x: d
                    .q8(t, "x")
                    .domain(a.x)
                    .range(t.horizontal ? o.y : o.x),
                  y: d
                    .q8(t, "y")
                    .domain(a.y)
                    .range(t.horizontal ? o.x : o.y),
                },
                c = e ? t.origin || v.IW(t) : void 0,
                l = m.Yu(t);
              return {
                style: r,
                data: (l = m.kQ(l, a, 0)),
                scale: i,
                domain: a,
                origin: c,
              };
            })(n),
          );
          var r = t,
            o = r.alignment,
            a = r.barRatio,
            i = r.cornerRadius,
            c = r.data,
            l = r.disableInlineStyles,
            u = r.domain,
            f = r.events,
            b = r.height,
            x = r.horizontal,
            O = r.origin,
            w = r.padding,
            C = r.polar,
            S = r.scale,
            A = r.sharedEvents,
            j = r.standalone,
            k = r.style,
            P = r.theme,
            E = r.width,
            M = r.labels,
            T = r.name,
            _ = r.barWidth,
            L = r.getPath,
            D = {
              parent: {
                horizontal: x,
                domain: u,
                scale: S,
                width: E,
                height: b,
                data: c,
                standalone: j,
                name: T,
                theme: P,
                polar: C,
                origin: O,
                padding: w,
                style: k.parent,
              },
            };
          return c.reduce(function (e, n, r) {
            var u = s()(n.eventKey) ? r : n.eventKey,
              y = (function (t, e) {
                var n = function (n) {
                    var r =
                        "log" === d.oL(t.scale[n])
                          ? 1 / Number.MAX_SAFE_INTEGER
                          : 0,
                      o = h.ao(t.domain[n]),
                      a = h.MN(t.domain[n]);
                    return (
                      o < 0 && a <= 0 ? (r = a) : o >= 0 && a > 0 && (r = o),
                      e["_".concat(n)] instanceof Date ? new Date(r) : r
                    );
                  },
                  r = void 0 !== e._y0 ? e._y0 : n("y"),
                  o = void 0 !== e._x0 ? e._x0 : n("x");
                return v.q2(t, p()({}, e, { _y0: r, _x0: o }));
              })(t, n),
              m = y.x,
              w = y.y,
              j = y.y0,
              P = y.x0,
              T = {
                alignment: o,
                barRatio: a,
                barWidth: _,
                cornerRadius: i,
                data: c,
                datum: n,
                disableInlineStyles: l,
                getPath: L,
                horizontal: x,
                index: r,
                polar: C,
                origin: O,
                scale: S,
                style: k.data,
                width: E,
                height: b,
                x: m,
                y: w,
                y0: j,
                x0: P,
              };
            e[u] = { data: T };
            var D = g.Q(t, n, r);
            return (
              ((void 0 !== D && null !== D) || (M && (f || A))) &&
                (e[u].labels = g.AM(t, r)),
              e
            );
          }, D);
        },
        x = n(46577),
        O = n(42017),
        w = n(93977),
        C = n.n(w),
        S = function (t, e) {
          var n = { topLeft: 0, topRight: 0, bottomLeft: 0, bottomRight: 0 };
          return t
            ? C()(t)
              ? (function (t, e) {
                  var n = {
                      topLeft: 0,
                      topRight: 0,
                      bottomLeft: 0,
                      bottomRight: 0,
                    },
                    r = function (r, o) {
                      s()(t[r])
                        ? s()(t[o]) || (n[r] = v.xs(t[o], e))
                        : (n[r] = v.xs(t[r], e));
                    };
                  return (
                    r("topLeft", "top"),
                    r("topRight", "top"),
                    r("bottomLeft", "bottom"),
                    r("bottomRight", "bottom"),
                    n
                  );
                })(t, e)
              : ((n.topLeft = v.xs(t, e)), (n.topRight = v.xs(t, e)), n)
            : n;
        };
      function A(t) {
        return function () {
          return t;
        };
      }
      const j = Math.abs,
        k = Math.atan2,
        P = Math.cos,
        E = Math.max,
        M = Math.min,
        T = Math.sin,
        _ = Math.sqrt,
        L = 1e-12,
        D = Math.PI,
        I = D / 2,
        R = 2 * D;
      function N(t) {
        return t >= 1 ? I : t <= -1 ? -I : Math.asin(t);
      }
      function W(t, e) {
        return (
          e || (e = t.slice(0)),
          Object.freeze(
            Object.defineProperties(t, { raw: { value: Object.freeze(e) } }),
          )
        );
      }
      var F, z, U, B, q, H, V, $, Y, Z, K, G, X, Q;
      const J = Math.PI,
        tt = 2 * J,
        et = 1e-6,
        nt = tt - et;
      function rt(t) {
        this._ += t[0];
        for (let e = 1, n = t.length; e < n; ++e) this._ += arguments[e] + t[e];
      }
      class ot {
        constructor(t) {
          (this._x0 = this._y0 = this._x1 = this._y1 = null),
            (this._ = ""),
            (this._append =
              null == t
                ? rt
                : (function (t) {
                    let e = Math.floor(t);
                    if (!(e >= 0))
                      throw new Error("invalid digits: ".concat(t));
                    if (e > 15) return rt;
                    const n = 10 ** e;
                    return function (t) {
                      this._ += t[0];
                      for (let e = 1, r = t.length; e < r; ++e)
                        this._ += Math.round(arguments[e] * n) / n + t[e];
                    };
                  })(t));
        }
        moveTo(t, e) {
          this._append(
            F || (F = W(["M", ",", ""])),
            (this._x0 = this._x1 = +t),
            (this._y0 = this._y1 = +e),
          );
        }
        closePath() {
          null !== this._x1 &&
            ((this._x1 = this._x0),
            (this._y1 = this._y0),
            this._append(z || (z = W(["Z"]))));
        }
        lineTo(t, e) {
          this._append(
            U || (U = W(["L", ",", ""])),
            (this._x1 = +t),
            (this._y1 = +e),
          );
        }
        quadraticCurveTo(t, e, n, r) {
          this._append(
            B || (B = W(["Q", ",", ",", ",", ""])),
            +t,
            +e,
            (this._x1 = +n),
            (this._y1 = +r),
          );
        }
        bezierCurveTo(t, e, n, r, o, a) {
          this._append(
            q || (q = W(["C", ",", ",", ",", ",", ",", ""])),
            +t,
            +e,
            +n,
            +r,
            (this._x1 = +o),
            (this._y1 = +a),
          );
        }
        arcTo(t, e, n, r, o) {
          if (((t = +t), (e = +e), (n = +n), (r = +r), (o = +o) < 0))
            throw new Error("negative radius: ".concat(o));
          let a = this._x1,
            i = this._y1,
            c = n - t,
            l = r - e,
            u = a - t,
            s = i - e,
            f = u * u + s * s;
          if (null === this._x1)
            this._append(
              H || (H = W(["M", ",", ""])),
              (this._x1 = t),
              (this._y1 = e),
            );
          else if (f > et)
            if (Math.abs(s * c - l * u) > et && o) {
              let p = n - a,
                d = r - i,
                h = c * c + l * l,
                v = p * p + d * d,
                y = Math.sqrt(h),
                m = Math.sqrt(f),
                g =
                  o * Math.tan((J - Math.acos((h + f - v) / (2 * y * m))) / 2),
                b = g / m,
                x = g / y;
              Math.abs(b - 1) > et &&
                this._append(
                  $ || ($ = W(["L", ",", ""])),
                  t + b * u,
                  e + b * s,
                ),
                this._append(
                  Y || (Y = W(["A", ",", ",0,0,", ",", ",", ""])),
                  o,
                  o,
                  +(s * p > u * d),
                  (this._x1 = t + x * c),
                  (this._y1 = e + x * l),
                );
            } else
              this._append(
                V || (V = W(["L", ",", ""])),
                (this._x1 = t),
                (this._y1 = e),
              );
          else;
        }
        arc(t, e, n, r, o, a) {
          if (((t = +t), (e = +e), (a = !!a), (n = +n) < 0))
            throw new Error("negative radius: ".concat(n));
          let i = n * Math.cos(r),
            c = n * Math.sin(r),
            l = t + i,
            u = e + c,
            s = 1 ^ a,
            f = a ? r - o : o - r;
          null === this._x1
            ? this._append(Z || (Z = W(["M", ",", ""])), l, u)
            : (Math.abs(this._x1 - l) > et || Math.abs(this._y1 - u) > et) &&
              this._append(K || (K = W(["L", ",", ""])), l, u),
            n &&
              (f < 0 && (f = (f % tt) + tt),
              f > nt
                ? this._append(
                    G ||
                      (G = W([
                        "A",
                        ",",
                        ",0,1,",
                        ",",
                        ",",
                        "A",
                        ",",
                        ",0,1,",
                        ",",
                        ",",
                        "",
                      ])),
                    n,
                    n,
                    s,
                    t - i,
                    e - c,
                    n,
                    n,
                    s,
                    (this._x1 = l),
                    (this._y1 = u),
                  )
                : f > et &&
                  this._append(
                    X || (X = W(["A", ",", ",0,", ",", ",", ",", ""])),
                    n,
                    n,
                    +(f >= J),
                    s,
                    (this._x1 = t + n * Math.cos(o)),
                    (this._y1 = e + n * Math.sin(o)),
                  ));
        }
        rect(t, e, n, r) {
          this._append(
            Q || (Q = W(["M", ",", "h", "v", "h", "Z"])),
            (this._x0 = this._x1 = +t),
            (this._y0 = this._y1 = +e),
            (n = +n),
            +r,
            -n,
          );
        }
        toString() {
          return this._;
        }
      }
      function at(t) {
        return t.innerRadius;
      }
      function it(t) {
        return t.outerRadius;
      }
      function ct(t) {
        return t.startAngle;
      }
      function lt(t) {
        return t.endAngle;
      }
      function ut(t) {
        return t && t.padAngle;
      }
      function st(t, e, n, r, o, a, i) {
        var c = t - n,
          l = e - r,
          u = (i ? a : -a) / _(c * c + l * l),
          s = u * l,
          f = -u * c,
          p = t + s,
          d = e + f,
          h = n + s,
          v = r + f,
          y = (p + h) / 2,
          m = (d + v) / 2,
          g = h - p,
          b = v - d,
          x = g * g + b * b,
          O = o - a,
          w = p * v - h * d,
          C = (b < 0 ? -1 : 1) * _(E(0, O * O * x - w * w)),
          S = (w * b - g * C) / x,
          A = (-w * g - b * C) / x,
          j = (w * b + g * C) / x,
          k = (-w * g + b * C) / x,
          P = S - y,
          M = A - m,
          T = j - y,
          L = k - m;
        return (
          P * P + M * M > T * T + L * L && ((S = j), (A = k)),
          {
            cx: S,
            cy: A,
            x01: -s,
            y01: -f,
            x11: S * (o / O - 1),
            y11: A * (o / O - 1),
          }
        );
      }
      function ft() {
        var t = at,
          e = it,
          n = A(0),
          r = null,
          o = ct,
          a = lt,
          i = ut,
          c = null,
          l = (function (t) {
            let e = 3;
            return (
              (t.digits = function (n) {
                if (!arguments.length) return e;
                if (null == n) e = null;
                else {
                  const t = Math.floor(n);
                  if (!(t >= 0))
                    throw new RangeError("invalid digits: ".concat(n));
                  e = t;
                }
                return t;
              }),
              () => new ot(e)
            );
          })(u);
        function u() {
          var u,
            s,
            f,
            p = +t.apply(this, arguments),
            d = +e.apply(this, arguments),
            h = o.apply(this, arguments) - I,
            v = a.apply(this, arguments) - I,
            y = j(v - h),
            m = v > h;
          if ((c || (c = u = l()), d < p && ((s = d), (d = p), (p = s)), d > L))
            if (y > R - L)
              c.moveTo(d * P(h), d * T(h)),
                c.arc(0, 0, d, h, v, !m),
                p > L &&
                  (c.moveTo(p * P(v), p * T(v)), c.arc(0, 0, p, v, h, m));
            else {
              var g,
                b,
                x = h,
                O = v,
                w = h,
                C = v,
                S = y,
                A = y,
                E = i.apply(this, arguments) / 2,
                W = E > L && (r ? +r.apply(this, arguments) : _(p * p + d * d)),
                F = M(j(d - p) / 2, +n.apply(this, arguments)),
                z = F,
                U = F;
              if (W > L) {
                var B = N((W / p) * T(E)),
                  q = N((W / d) * T(E));
                (S -= 2 * B) > L
                  ? ((w += B *= m ? 1 : -1), (C -= B))
                  : ((S = 0), (w = C = (h + v) / 2)),
                  (A -= 2 * q) > L
                    ? ((x += q *= m ? 1 : -1), (O -= q))
                    : ((A = 0), (x = O = (h + v) / 2));
              }
              var H = d * P(x),
                V = d * T(x),
                $ = p * P(C),
                Y = p * T(C);
              if (F > L) {
                var Z,
                  K = d * P(O),
                  G = d * T(O),
                  X = p * P(w),
                  Q = p * T(w);
                if (y < D)
                  if (
                    (Z = (function (t, e, n, r, o, a, i, c) {
                      var l = n - t,
                        u = r - e,
                        s = i - o,
                        f = c - a,
                        p = f * l - s * u;
                      if (!(p * p < L))
                        return [
                          t + (p = (s * (e - a) - f * (t - o)) / p) * l,
                          e + p * u,
                        ];
                    })(H, V, X, Q, K, G, $, Y))
                  ) {
                    var J = H - Z[0],
                      tt = V - Z[1],
                      et = K - Z[0],
                      nt = G - Z[1],
                      rt =
                        1 /
                        T(
                          ((f =
                            (J * et + tt * nt) /
                            (_(J * J + tt * tt) * _(et * et + nt * nt))) > 1
                            ? 0
                            : f < -1
                              ? D
                              : Math.acos(f)) / 2,
                        ),
                      ot = _(Z[0] * Z[0] + Z[1] * Z[1]);
                    (z = M(F, (p - ot) / (rt - 1))),
                      (U = M(F, (d - ot) / (rt + 1)));
                  } else z = U = 0;
              }
              A > L
                ? U > L
                  ? ((g = st(X, Q, H, V, d, U, m)),
                    (b = st(K, G, $, Y, d, U, m)),
                    c.moveTo(g.cx + g.x01, g.cy + g.y01),
                    U < F
                      ? c.arc(
                          g.cx,
                          g.cy,
                          U,
                          k(g.y01, g.x01),
                          k(b.y01, b.x01),
                          !m,
                        )
                      : (c.arc(
                          g.cx,
                          g.cy,
                          U,
                          k(g.y01, g.x01),
                          k(g.y11, g.x11),
                          !m,
                        ),
                        c.arc(
                          0,
                          0,
                          d,
                          k(g.cy + g.y11, g.cx + g.x11),
                          k(b.cy + b.y11, b.cx + b.x11),
                          !m,
                        ),
                        c.arc(
                          b.cx,
                          b.cy,
                          U,
                          k(b.y11, b.x11),
                          k(b.y01, b.x01),
                          !m,
                        )))
                  : (c.moveTo(H, V), c.arc(0, 0, d, x, O, !m))
                : c.moveTo(H, V),
                p > L && S > L
                  ? z > L
                    ? ((g = st($, Y, K, G, p, -z, m)),
                      (b = st(H, V, X, Q, p, -z, m)),
                      c.lineTo(g.cx + g.x01, g.cy + g.y01),
                      z < F
                        ? c.arc(
                            g.cx,
                            g.cy,
                            z,
                            k(g.y01, g.x01),
                            k(b.y01, b.x01),
                            !m,
                          )
                        : (c.arc(
                            g.cx,
                            g.cy,
                            z,
                            k(g.y01, g.x01),
                            k(g.y11, g.x11),
                            !m,
                          ),
                          c.arc(
                            0,
                            0,
                            p,
                            k(g.cy + g.y11, g.cx + g.x11),
                            k(b.cy + b.y11, b.cx + b.x11),
                            m,
                          ),
                          c.arc(
                            b.cx,
                            b.cy,
                            z,
                            k(b.y11, b.x11),
                            k(b.y01, b.x01),
                            !m,
                          )))
                    : c.arc(0, 0, p, C, w, m)
                  : c.lineTo($, Y);
            }
          else c.moveTo(0, 0);
          if ((c.closePath(), u)) return (c = null), u + "" || null;
        }
        return (
          (u.centroid = function () {
            var n = (+t.apply(this, arguments) + +e.apply(this, arguments)) / 2,
              r =
                (+o.apply(this, arguments) + +a.apply(this, arguments)) / 2 -
                D / 2;
            return [P(r) * n, T(r) * n];
          }),
          (u.innerRadius = function (e) {
            return arguments.length
              ? ((t = "function" === typeof e ? e : A(+e)), u)
              : t;
          }),
          (u.outerRadius = function (t) {
            return arguments.length
              ? ((e = "function" === typeof t ? t : A(+t)), u)
              : e;
          }),
          (u.cornerRadius = function (t) {
            return arguments.length
              ? ((n = "function" === typeof t ? t : A(+t)), u)
              : n;
          }),
          (u.padRadius = function (t) {
            return arguments.length
              ? ((r = null == t ? null : "function" === typeof t ? t : A(+t)),
                u)
              : r;
          }),
          (u.startAngle = function (t) {
            return arguments.length
              ? ((o = "function" === typeof t ? t : A(+t)), u)
              : o;
          }),
          (u.endAngle = function (t) {
            return arguments.length
              ? ((a = "function" === typeof t ? t : A(+t)), u)
              : a;
          }),
          (u.padAngle = function (t) {
            return arguments.length
              ? ((i = "function" === typeof t ? t : A(+t)), u)
              : i;
          }),
          (u.context = function (t) {
            return arguments.length ? ((c = null == t ? null : t), u) : c;
          }),
          u
        );
      }
      ot.prototype;
      var pt = function (t, e) {
          return {
            x: t,
            y: e,
            distance: function (t) {
              return Math.sqrt(
                Math.pow(this.x - t.x, 2) + Math.pow(this.y - t.y, 2),
              );
            },
            add: function (t) {
              return pt(this.x + t.x, this.y + t.y);
            },
            subtract: function (t) {
              return pt(this.x - t.x, this.y - t.y);
            },
            scalarMult: function (t) {
              return pt(this.x * t, this.y * t);
            },
            scalarDivide: function (t) {
              if (0 === t) throw new Error("Division by 0 error");
              return pt(this.x / t, this.y / t);
            },
            equals: function (t) {
              return this.x === t.x && this.y === t.y;
            },
          };
        },
        dt = function (t, e) {
          return {
            center: t,
            radius: e,
            hasIntersection: function (t) {
              var e = this.center,
                n = t.center,
                r = this.radius,
                o = t.radius,
                a = e.distance(n);
              return !(a > r + o) && !(a < Math.abs(r - o));
            },
            equals: function (t) {
              var e = this.center,
                n = t.center;
              return this.radius === t.radius && e.equals(n);
            },
            intersection: function (t) {
              var e = this.center,
                n = t.center,
                r = this.radius,
                o = t.radius,
                a = e.distance(n);
              if (!this.hasIntersection(t) || this.equals(t)) return [];
              var i =
                  (Math.pow(r, 2) - Math.pow(o, 2) + Math.pow(a, 2)) / (2 * a),
                c = Math.sqrt(Math.pow(r, 2) - Math.pow(i, 2)),
                l = e.add(n.subtract(e).scalarMult(i).scalarDivide(a)),
                u = e.x,
                s = e.y,
                f = n.x,
                p = n.y,
                d = l.x,
                h = l.y,
                v = [
                  pt(d - (c * (p - s)) / a, h + (c * (f - u)) / a),
                  pt(d + (c * (p - s)) / a, h - (c * (f - u)) / a),
                ];
              return (
                v.sort(function (t, e) {
                  return t.x - e.x;
                }),
                v
              );
            },
            solveX: function (t) {
              var e = Math.sqrt(
                Math.pow(this.radius, 2) - Math.pow(t - this.center.y, 2),
              );
              return [this.center.x - e, this.center.x + e];
            },
            solveY: function (t) {
              var e = Math.sqrt(
                Math.pow(this.radius, 2) - Math.pow(t - this.center.x, 2),
              );
              return [this.center.y - e, this.center.y + e];
            },
          };
        };
      function ht(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function vt(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? ht(Object(n), !0).forEach(function (e) {
                yt(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : ht(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function yt(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      function mt(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return gt(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return gt(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return gt(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function gt(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      var bt = function (t, e) {
          var n = t.x,
            r = t.x0,
            o = t.y,
            a = t.y0,
            i = t.horizontal,
            c = t.alignment || "middle",
            l = "middle" === c ? e / 2 : e,
            u = i ? -1 : 1;
          return i
            ? {
                x0: r,
                x1: n,
                y0: "start" === c ? o : o - u * l,
                y1: "end" === c ? o : o + u * l,
              }
            : {
                x0: "start" === c ? n : n - u * l,
                x1: "end" === c ? n : n + u * l,
                y0: a,
                y1: o,
              };
        },
        xt = function (t, e) {
          var n = t.data,
            r = t.scale,
            o = void 0 === n[e]._x1 ? "_x" : "_x1";
          return r.x(n[e][o]);
        },
        Ot = function (t) {
          return -1 * t + Math.PI / 2;
        },
        wt = function (t, e, n) {
          var r = "".concat(e.topLeft, " ").concat(e.topLeft, " ").concat(n),
            o = "".concat(e.topRight, " ").concat(e.topRight, " ").concat(n),
            a = ""
              .concat(e.bottomLeft, " ")
              .concat(e.bottomLeft, " ")
              .concat(n),
            i = ""
              .concat(e.bottomRight, " ")
              .concat(e.bottomRight, " ")
              .concat(n),
            c = [
              "M",
              "A ".concat(a, ","),
              "L",
              "A ".concat(r, ","),
              "L",
              "A ".concat(o, ","),
              "L",
              "A ".concat(i, ","),
            ].reduce(function (e, n, r) {
              return (e += ""
                .concat(n, " ")
                .concat(t[r].x, ", ")
                .concat(t[r].y, " \n"));
            }, "");
          return "".concat(c, " z");
        },
        Ct = function (t, e, n) {
          var r = bt(t, e),
            o = r.y0 > r.y1 ? 1 : -1,
            a = o > 0 ? "0 0 1" : "0 0 0",
            i = (function (t, e, n) {
              var r = t.x0,
                o = t.x1,
                a = t.y0,
                i = t.y1,
                c = function (t) {
                  var c = "Left" === t,
                    l = c ? 1 : -1,
                    u = c ? r : o,
                    s = { x: u + l * n["bottom".concat(t)], y: a },
                    f = { x: u, y: a - e * n["bottom".concat(t)] },
                    p = { x: u, y: i + e * n["top".concat(t)] },
                    d = { x: u + l * n["top".concat(t)], y: i };
                  if (
                    1 === e
                      ? a - n["bottom".concat(t)] < i + n["top".concat(t)]
                      : a + n["bottom".concat(t)] > i - n["top".concat(t)]
                  ) {
                    var h = pt(
                        u + l * n["top".concat(t)],
                        i + e * n["top".concat(t)],
                      ),
                      v = dt(h, n["top".concat(t)]),
                      y = pt(
                        u + l * n["bottom".concat(t)],
                        a - e * n["bottom".concat(t)],
                      ),
                      m = dt(y, n["bottom".concat(t)]),
                      g = v.intersection(m);
                    if (g.length > 0) {
                      var b = g[c ? 0 : 1];
                      (f = { x: b.x, y: b.y }), (p = { x: b.x, y: b.y });
                    } else if (n["top".concat(t)] > n["bottom".concat(t)]) {
                      var x = v.solveX(a)[c ? 0 : 1];
                      (s = { x: x, y: a }),
                        (f = { x: x, y: a }),
                        (p = { x: x, y: a });
                    } else {
                      var O = m.solveX(i)[c ? 0 : 1];
                      (f = { x: O, y: i }),
                        (p = { x: O, y: i }),
                        (d = { x: O, y: i });
                    }
                  }
                  var w = [s, f, p, d];
                  return c ? w : w.reverse();
                };
              return c("Left").concat(c("Right"));
            })(r, o, n);
          return wt(i, n, a);
        },
        St = function (t, e, n) {
          var r = bt(t, e),
            o = r.x0 < r.x1 ? 1 : -1,
            a = {
              topRight: o > 0 ? n.topLeft : n.bottomLeft,
              bottomRight: o > 0 ? n.topRight : n.bottomRight,
              bottomLeft: o > 0 ? n.bottomRight : n.topRight,
              topLeft: o > 0 ? n.bottomLeft : n.topLeft,
            },
            i = (function (t, e, n) {
              var r = t.y0,
                o = t.y1,
                a = t.x0 < t.x1 ? t.x0 : t.x1,
                i = t.x0 < t.x1 ? t.x1 : t.x0,
                c = function (t) {
                  var c = "top" === t,
                    l = c ? -1 : 1,
                    u = c ? o : r,
                    s = { x: a, y: u - l * n["".concat(t, "Left")] },
                    f = { x: a + n["".concat(t, "Left")], y: u },
                    p = { x: i - n["".concat(t, "Right")], y: u },
                    d = { x: i, y: u - l * n["".concat(t, "Right")] };
                  if (f.x > p.x) {
                    var h = pt(
                        a + n["".concat(t, "Left")],
                        u - l * n["".concat(t, "Left")],
                      ),
                      v = dt(h, n["".concat(t, "Left")]),
                      y = pt(
                        i - n["".concat(t, "Right")],
                        u - l * n["".concat(t, "Right")],
                      ),
                      m = dt(y, n["".concat(t, "Right")]),
                      g = v.intersection(m);
                    if (g.length > 0) {
                      var b = g[e > 0 ? 1 : 0];
                      (f = { x: b.x, y: b.y }), (p = { x: b.x, y: b.y });
                    } else if (
                      n["".concat(t, "Right")] > n["".concat(t, "Left")]
                    ) {
                      var x = m.solveY(a)[c ? 0 : 1];
                      (s = { x: a, y: x }),
                        (f = { x: a, y: x }),
                        (p = { x: a, y: x });
                    } else {
                      var O = v.solveY(i)[c ? 0 : 1];
                      (d = { x: i, y: O }),
                        (p = { x: i, y: O }),
                        (f = { x: i, y: O });
                    }
                  }
                  return [s, f, p, d];
                },
                l = c("top"),
                u = c("bottom");
              return [u[1], u[0]].concat(mt(l), [u[3], u[2]]);
            })(r, o, a);
          return wt(i, a, "0 0 1");
        },
        At = function (t, e) {
          var n,
            r,
            o = t.datum,
            a = t.scale,
            i = t.index,
            c = t.alignment,
            l = t.style,
            u = a.y(o._y0 || 0),
            s = a.y(void 0 !== o._y1 ? o._y1 : o._y),
            f = a.x(void 0 !== o._x1 ? o._x1 : o._x);
          if (l.width) {
            var p = (function (t, e) {
                var n = t.scale,
                  r = n.y.range(),
                  o = Math.max.apply(Math, mt(r)),
                  a = Math.abs(n.x.range()[1] - n.x.range()[0]);
                return (e / (2 * Math.PI * o)) * a;
              })(t, l.width),
              d = "middle" === c ? p / 2 : p;
            (n = "start" === c ? f : f - d), (r = "end" === c ? f : f + d);
          } else
            (n = (function (t, e) {
              var n = t.data,
                r = t.scale,
                o = t.alignment,
                a = xt(t, e),
                i = Math.abs(r.x.range()[1] - r.x.range()[0]),
                c = 0 === e ? xt(t, n.length - 1) - 2 * Math.PI : xt(t, e - 1);
              return 0 === e && i < 2 * Math.PI
                ? r.x.range()[0]
                : "start" === o || "end" === o
                  ? "start" === o
                    ? c
                    : a
                  : (a + c) / 2;
            })(t, i)),
              (r = (function (t, e) {
                var n = t.data,
                  r = t.scale,
                  o = t.alignment,
                  a = xt(t, e),
                  i = Math.abs(r.x.range()[1] - r.x.range()[0]),
                  c =
                    r.x.range()[1] === 2 * Math.PI
                      ? xt(t, 0) + 2 * Math.PI
                      : r.x.range()[1],
                  l =
                    e === n.length - 1 ? xt(t, 0) + 2 * Math.PI : xt(t, e + 1);
                return e === n.length - 1 && i < 2 * Math.PI
                  ? c
                  : "start" === o || "end" === o
                    ? "start" === o
                      ? a
                      : l
                    : (a + l) / 2;
              })(t, i));
          var h = function (t) {
              return ft()
                .innerRadius(u)
                .outerRadius(s)
                .startAngle(Ot(n))
                .endAngle(Ot(r))
                .cornerRadius(e[t])();
            },
            v = function (t) {
              var e = h("".concat(t, "Right")),
                n = e.match(/[A-Z]/g),
                r = e.split(/[A-Z]/).slice(1),
                o = n.indexOf("L"),
                a = h("".concat(t, "Left")),
                i = a.match(/[A-Z]/g),
                c = a.split(/[A-Z]/).slice(1),
                l = i.indexOf("L");
              return {
                rightMoves: n,
                rightCoords: r,
                rightMiddle: o,
                leftMoves: i,
                leftCoords: c,
                leftMiddle: l,
              };
            },
            y = (function () {
              var t,
                o,
                a = e.topRight,
                i = e.topLeft,
                c = s * Math.abs(r - n),
                l = v("top"),
                u = l.rightMoves,
                f = l.rightCoords,
                p = l.rightMiddle,
                d = l.leftMoves,
                h = l.leftCoords,
                y = l.leftMiddle;
              if (a === i || c < 2 * a + 2 * i)
                (t = a > i ? u : d), (o = a > i ? f : h);
              else {
                var m,
                  g = function (t) {
                    return t < 3;
                  },
                  b = i > a && g(p) ? 1 : 2;
                if (a > i) {
                  var x = g(p) ? y : y - 2;
                  m = g(y) ? y - 1 : x;
                } else {
                  var O = g(y) ? 1 : 2;
                  m = g(p) ? O : y - 2;
                }
                (t = [].concat(mt(u.slice(0, b)), mt(d.slice(m)))),
                  (o = [].concat(mt(f.slice(0, b)), mt(h.slice(m))));
              }
              var w = t.indexOf("L"),
                C = t.slice(0, w),
                S = o.slice(0, w);
              return C.map(function (t, e) {
                return { command: t, coords: S[e].split(",") };
              });
            })(),
            m = (function () {
              var t,
                o,
                a = e.bottomRight,
                i = e.bottomLeft,
                c = u * Math.abs(r - n),
                l = v("bottom"),
                s = l.rightMoves,
                f = l.rightCoords,
                p = l.rightMiddle,
                d = l.leftMoves,
                h = l.leftCoords,
                y = l.leftMiddle;
              if (a === i || c < 2 * a + 2 * i)
                (t = a > i ? s : d), (o = a > i ? f : h);
              else {
                var m = function (t, e) {
                    return t.length - e < 4;
                  },
                  g = (a > i ? m(s, p) : m(d, y)) ? -1 : -3;
                (t = [].concat(mt(d.slice(0, y + 2)), mt(s.slice(g)))),
                  (o = [].concat(mt(h.slice(0, y + 2)), mt(f.slice(g))));
              }
              var b = t.indexOf("L"),
                x = t.slice(b, -1),
                O = o.slice(b, -1);
              return x.map(function (t, e) {
                return { command: t, coords: O[e].split(",") };
              });
            })(),
            g = [].concat(mt(y), mt(m)).reduce(function (t, e) {
              return (t += "".concat(e.command, " ").concat(e.coords.join()));
            }, "");
          return "".concat(g, " z");
        },
        jt = function (t, e, n) {
          return t.getPath
            ? (function (t, e) {
                return (0, t.getPath)(vt(vt({}, t), bt(t, e)));
              })(t, e)
            : t.horizontal
              ? St(t, e, n)
              : Ct(t, e, n);
        };
      function kt(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function Pt(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? kt(Object(n), !0).forEach(function (e) {
                Et(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : kt(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function Et(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      var Mt = function (t) {
          var e = (function () {
              var t =
                  arguments.length > 0 && void 0 !== arguments[0]
                    ? arguments[0]
                    : {},
                e = arguments.length > 1 ? arguments[1] : void 0;
              if (e.disableInlineStyles) return {};
              var n = { fill: "black", stroke: t.fill || "black" };
              return v.F3(p()(n, t), e);
            })(t.style, t),
            n = (function (t, e) {
              var n = e.scale,
                r = e.data,
                o = e.defaultBarWidth,
                a = e.style;
              if (t) return v.xs(t, e);
              if (a.width) return a.width;
              var i = n.x.range(),
                c = Math.abs(i[1] - i[0]),
                l = r.length + 2,
                u = (e.barRatio || 0.5) * (r.length < 2 ? o : c / l);
              return Math.max(1, u);
            })(t.barWidth, p()({}, t, { style: e })),
            r = S(t.cornerRadius, p()({}, t, { style: e, barWidth: n })),
            o = v.xs(t.ariaLabel, t),
            a = v.xs(t.desc, t),
            i = v.xs(t.id, t),
            c = v.xs(t.tabIndex, t);
          return p()({}, t, {
            ariaLabel: o,
            style: e,
            barWidth: n,
            cornerRadius: r,
            desc: a,
            id: i,
            tabIndex: c,
          });
        },
        Tt = (0, o.forwardRef)(function (t, e) {
          var n = (t = Mt(t)),
            r = n.polar,
            a = n.origin,
            i = n.style,
            c = n.barWidth,
            l = n.cornerRadius,
            u = r
              ? (function (t, e) {
                  return At(t, e);
                })(t, l)
              : jt(t, c, l),
            s =
              r && a ? "translate(".concat(a.x, ", ").concat(a.y, ")") : void 0;
          return o.cloneElement(
            t.pathComponent,
            Pt(
              Pt({}, t.events),
              {},
              {
                "aria-label": t.ariaLabel,
                style: i,
                d: u,
                className: t.className,
                clipPath: t.clipPath,
                desc: t.desc,
                index: t.index,
                role: t.role,
                shapeRendering: t.shapeRendering,
                transform: t.transform || s,
                tabIndex: t.tabIndex,
                ref: e,
              },
            ),
          );
        });
      (Tt.propTypes = Pt(
        Pt({}, x.l.primitiveProps),
        {},
        {
          alignment: l().oneOf(["start", "middle", "end"]),
          barRatio: l().number,
          barWidth: l().oneOfType([l().number, l().func]),
          cornerRadius: l().oneOfType([
            l().number,
            l().func,
            l().shape({
              top: l().oneOfType([l().number, l().func]),
              topLeft: l().oneOfType([l().number, l().func]),
              topRight: l().oneOfType([l().number, l().func]),
              bottom: l().oneOfType([l().number, l().func]),
              bottomLeft: l().oneOfType([l().number, l().func]),
              bottomRight: l().oneOfType([l().number, l().func]),
            }),
          ]),
          datum: l().object,
          getPath: l().func,
          horizontal: l().bool,
          pathComponent: l().element,
          width: l().number,
          x: l().number,
          y: l().number,
          y0: l().number,
        },
      )),
        (Tt.defaultProps = {
          defaultBarWidth: 8,
          pathComponent: o.createElement(O.y, null),
          role: "presentation",
          shapeRendering: "auto",
        });
      const _t = Tt;
      var Lt = n(97409),
        Dt = n(17792),
        It = n(83485),
        Rt = n(58853),
        Nt = n(86225);
      function Wt(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function Ft(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? Wt(Object(n), !0).forEach(function (e) {
                zt(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : Wt(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function zt(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      function Ut(t, e) {
        for (var n = 0; n < e.length; n++) {
          var r = e[n];
          (r.enumerable = r.enumerable || !1),
            (r.configurable = !0),
            "value" in r && (r.writable = !0),
            Object.defineProperty(t, r.key, r);
        }
      }
      function Bt(t, e) {
        return (
          (Bt = Object.setPrototypeOf
            ? Object.setPrototypeOf.bind()
            : function (t, e) {
                return (t.__proto__ = e), t;
              }),
          Bt(t, e)
        );
      }
      function qt(t) {
        var e = (function () {
          if ("undefined" === typeof Reflect || !Reflect.construct) return !1;
          if (Reflect.construct.sham) return !1;
          if ("function" === typeof Proxy) return !0;
          try {
            return (
              Boolean.prototype.valueOf.call(
                Reflect.construct(Boolean, [], function () {}),
              ),
              !0
            );
          } catch (t) {
            return !1;
          }
        })();
        return function () {
          var n,
            r = Ht(t);
          if (e) {
            var o = Ht(this).constructor;
            n = Reflect.construct(r, arguments, o);
          } else n = r.apply(this, arguments);
          return (function (t, e) {
            if (e && ("object" === typeof e || "function" === typeof e))
              return e;
            if (void 0 !== e)
              throw new TypeError(
                "Derived constructors may only return object or undefined",
              );
            return (function (t) {
              if (void 0 === t)
                throw new ReferenceError(
                  "this hasn't been initialised - super() hasn't been called",
                );
              return t;
            })(t);
          })(this, n);
        };
      }
      function Ht(t) {
        return (
          (Ht = Object.setPrototypeOf
            ? Object.getPrototypeOf.bind()
            : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t);
              }),
          Ht(t)
        );
      }
      var Vt = { width: 450, height: 300, padding: 50 },
        $t = (function (t) {
          !(function (t, e) {
            if ("function" !== typeof e && null !== e)
              throw new TypeError(
                "Super expression must either be null or a function",
              );
            (t.prototype = Object.create(e && e.prototype, {
              constructor: { value: t, writable: !0, configurable: !0 },
            })),
              Object.defineProperty(t, "prototype", { writable: !1 }),
              e && Bt(t, e);
          })(a, t);
          var e,
            n,
            r,
            o = qt(a);
          function a() {
            return (
              (function (t, e) {
                if (!(t instanceof e))
                  throw new TypeError("Cannot call a class as a function");
              })(this, a),
              o.apply(this, arguments)
            );
          }
          return (
            (e = a),
            (n = [
              {
                key: "shouldAnimate",
                value: function () {
                  return !!this.props.animate;
                },
              },
              {
                key: "render",
                value: function () {
                  var t = a.animationWhitelist,
                    e = a.role,
                    n = v.TY(this.props, Vt, e);
                  if (this.shouldAnimate()) return this.animateComponent(n, t);
                  var r = this.renderData(n),
                    o = n.standalone
                      ? this.renderContainer(n.containerComponent, r)
                      : r;
                  return Lt.h(o, n);
                },
              },
            ]) && Ut(e.prototype, n),
            r && Ut(e, r),
            Object.defineProperty(e, "prototype", { writable: !1 }),
            a
          );
        })(o.Component);
      ($t.animationWhitelist = [
        "data",
        "domain",
        "height",
        "padding",
        "style",
        "width",
      ]),
        ($t.displayName = "VictoryBar"),
        ($t.role = "bar"),
        ($t.defaultTransitions = {
          onLoad: {
            duration: 2e3,
            before: function () {
              return { _y: 0, _y1: 0, _y0: 0 };
            },
            after: function (t) {
              return { _y: t._y, _y1: t._y1, _y0: t._y0 };
            },
          },
          onExit: {
            duration: 500,
            before: function () {
              return { _y: 0, yOffset: 0 };
            },
          },
          onEnter: {
            duration: 500,
            before: function () {
              return { _y: 0, _y1: 0, _y0: 0 };
            },
            after: function (t) {
              return { _y: t._y, _y1: t._y1, _y0: t._y0 };
            },
          },
        }),
        ($t.propTypes = Ft(
          Ft(Ft({}, x.l.baseProps), x.l.dataProps),
          {},
          {
            alignment: l().oneOf(["start", "middle", "end"]),
            barRatio: l().number,
            barWidth: l().oneOfType([l().number, l().func]),
            cornerRadius: l().oneOfType([
              l().number,
              l().func,
              l().shape({
                top: l().oneOfType([l().number, l().func]),
                topLeft: l().oneOfType([l().number, l().func]),
                topRight: l().oneOfType([l().number, l().func]),
                bottom: l().oneOfType([l().number, l().func]),
                bottomLeft: l().oneOfType([l().number, l().func]),
                bottomRight: l().oneOfType([l().number, l().func]),
              }),
            ]),
            getPath: l().func,
            horizontal: l().bool,
          },
        )),
        ($t.defaultProps = {
          containerComponent: o.createElement(Dt._, null),
          data: [
            { x: 1, y: 1 },
            { x: 2, y: 2 },
            { x: 3, y: 3 },
            { x: 4, y: 4 },
          ],
          dataComponent: o.createElement(_t, null),
          groupComponent: o.createElement("g", { role: "presentation" }),
          labelComponent: o.createElement(It.X, null),
          samples: 50,
          sortOrder: "ascending",
          standalone: !0,
          theme: Rt.J.grayscale,
        }),
        ($t.getDomain = y.x1),
        ($t.getData = m.Yu),
        ($t.getBaseProps = function (t) {
          return b(t, Vt);
        }),
        ($t.expectedComponents = [
          "dataComponent",
          "labelComponent",
          "groupComponent",
          "containerComponent",
        ]);
      const Yt = (0, Nt.o)($t);
      var Zt = n(50235),
        Kt = n(79674);
      const Gt = (t) => {
        var {
            containerComponent: e = o.createElement(Zt.B, null),
            themeColor: n,
            theme: a = (0, Kt.gh)(n),
          } = t,
          i = (0, r.__rest)(t, ["containerComponent", "themeColor", "theme"]);
        const c = o.cloneElement(e, Object.assign({ theme: a }, e.props));
        return o.createElement(
          Yt,
          Object.assign({ containerComponent: c, theme: a }, i),
        );
      };
      (Gt.displayName = "ChartBar"), i()(Gt, Yt);
    },
    50235: (t, e, n) => {
      "use strict";
      n.d(e, { B: () => s });
      var r = n(75971),
        o = n(72791),
        a = n(62110),
        i = n.n(a),
        c = n(17792),
        l = n(79674),
        u = n(70219);
      const s = (t) => {
        var { className: e, themeColor: n, theme: a = (0, l.gh)(n) } = t,
          i = (0, r.__rest)(t, ["className", "themeColor", "theme"]);
        const s = (0, u.g)({ className: e });
        return o.createElement(
          c._,
          Object.assign({ className: s, theme: a }, i),
        );
      };
      (s.displayName = "ChartContainer"), i()(s, c._);
    },
    54149: (t, e, n) => {
      "use strict";
      n.d(e, { G: () => tt });
      var r = n(75971),
        o = n(72791),
        a = n(62110),
        i = n.n(a),
        c = n(66364),
        l = n.n(c),
        u = n(66933),
        s = n.n(u),
        f = n(15687),
        p = n.n(f),
        d = n(52007),
        h = n.n(d),
        v = n(78457),
        y = n(8091),
        m = n(97409),
        g = n(71472),
        b = n(70295),
        x = n(46577),
        O = n(17792),
        w = n(58853),
        C = n(68973),
        S = n(20933),
        A = n(54481),
        j = n(50077),
        k = n.n(j);
      function P(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return T(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          M(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function E(t, e) {
        return (
          (function (t) {
            if (Array.isArray(t)) return t;
          })(t) ||
          (function (t, e) {
            var n =
              null == t
                ? null
                : ("undefined" !== typeof Symbol && t[Symbol.iterator]) ||
                  t["@@iterator"];
            if (null == n) return;
            var r,
              o,
              a = [],
              i = !0,
              c = !1;
            try {
              for (
                n = n.call(t);
                !(i = (r = n.next()).done) &&
                (a.push(r.value), !e || a.length !== e);
                i = !0
              );
            } catch (l) {
              (c = !0), (o = l);
            } finally {
              try {
                i || null == n.return || n.return();
              } finally {
                if (c) throw o;
              }
            }
            return a;
          })(t, e) ||
          M(t, e) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function M(t, e) {
        if (t) {
          if ("string" === typeof t) return T(t, e);
          var n = Object.prototype.toString.call(t).slice(8, -1);
          return (
            "Object" === n && t.constructor && (n = t.constructor.name),
            "Map" === n || "Set" === n
              ? Array.from(t)
              : "Arguments" === n ||
                  /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
                ? T(t, e)
                : void 0
          );
        }
      }
      function T(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function _(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function L(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? _(Object(n), !0).forEach(function (e) {
                D(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : _(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function D(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      var I = { width: 450, height: 300, padding: 50, offset: 0 };
      function R(t, e) {
        var n = "group";
        t = y.TY(t, I, n);
        var r = g.C2(t.theme, t.style, n),
          o = t,
          a = o.offset,
          i = o.colorScale,
          c = o.color,
          l = o.polar,
          u = o.horizontal,
          s = t.categories || g.CP(t, e, null),
          f = t.datasets || g.D8(t, null),
          d = {
            x: g.ge(p()({}, t, { categories: s }), "x", e),
            y: g.ge(p()({}, t, { categories: s }), "y", e),
          },
          h = t.range || { x: y.rx(t, "x"), y: y.rx(t, "y") },
          v = {
            x: S.j$(t, "x") || g.yZ(t, "x"),
            y: S.j$(t, "y") || g.yZ(t, "y"),
          };
        return {
          datasets: f,
          categories: s,
          range: h,
          domain: d,
          horizontal: u,
          scale: {
            x: v.x.domain(d.x).range(t.horizontal ? h.y : h.x),
            y: v.y.domain(d.y).range(t.horizontal ? h.x : h.y),
          },
          style: r,
          colorScale: i,
          color: c,
          offset: a,
          origin: l ? t.origin : y.IW(t),
          padding: y.tQ(t),
        };
      }
      function N(t) {
        var e = (function (t) {
            var e = t.children,
              n = o.Children.toArray(e).map(function (t) {
                return L(
                  L({}, t),
                  {},
                  { props: y.CE(t.props, ["sharedEvents"]) },
                );
              });
            return (t.children = n), t;
          })(t),
          n = E(o.useState(e), 2),
          r = n[0],
          a = n[1];
        return (
          o.useEffect(
            function () {
              k()(e, r) || a(e);
            },
            [r, a, e],
          ),
          o.useMemo(
            function () {
              return R(r, r.children);
            },
            [r],
          )
        );
      }
      function W(t, e, n, r) {
        var o =
            (("stack" === r ? e.datasets[0].length : e.datasets.length) - 1) /
            2,
          a = (function (t, e, n) {
            if (!t.offset) return 0;
            var r = y.Uk(e, t.horizontal),
              o = n.domain[e],
              a = n.range[r];
            return (
              ((Math.max.apply(Math, P(o)) - Math.min.apply(Math, P(o))) /
                (Math.max.apply(Math, P(a)) - Math.min.apply(Math, P(a)))) *
              t.offset
            );
          })(t, "x", e);
        return (n - o) * a;
      }
      function F(t, e, n, r) {
        var o =
            (("stack" === r ? e.datasets[0].length : e.datasets.length) - 1) /
            2,
          a = (function (t, e) {
            var n = e.range,
              r = Math.abs(n.x[1] - n.x[0]),
              o = Math.max.apply(Math, P(n.y));
            return (t.offset / (2 * Math.PI * o)) * r;
          })(t, e);
        return (n - o) * a;
      }
      function z(t, e) {
        var n = e.type && e.type.role,
          r = e.props.colorScale || t.colorScale;
        if ("group" === n || "stack" === n)
          return t.theme && t.theme.group ? r || t.theme.group.colorScale : r;
      }
      function U(t) {
        var e =
            arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : [],
          n = arguments.length > 2 ? arguments[2] : void 0,
          r = t.data || t.y ? A.Yu(t) : e,
          o = n || 0;
        return r.map(function (t) {
          var e =
            t._x instanceof Date ? new Date(t._x.getTime() + o) : t._x + o;
          return p()({}, t, { _x1: e });
        });
      }
      function B(t, e, n) {
        (t = y.TY(t, I, "stack")), (e = e || o.Children.toArray(t.children));
        var r = (n = n || R(t, e)).datasets,
          a = t,
          i = a.labelComponent,
          c = a.polar,
          l = (function (t, e) {
            var n = e.categories,
              r = e.domain,
              o = e.range,
              a = e.scale,
              i = e.horizontal,
              c = e.origin,
              l = e.padding,
              u = t.width;
            return {
              height: t.height,
              width: u,
              theme: t.theme,
              polar: t.polar,
              origin: c,
              categories: n,
              domain: r,
              range: o,
              scale: a,
              horizontal: i,
              padding: l,
              standalone: !1,
            };
          })(t, n),
          u = t.name || "group";
        return e.map(function (e, a) {
          var s = e.type && e.type.role,
            f = c ? F(t, n, a, s) : W(t, n, a, s),
            d =
              "voronoi" === s || "tooltip" === s || "label" === s
                ? e.props.style
                : g.ny(e, a, n),
            h = t.labels
              ? (function (t, e, n) {
                  if (t.labels)
                    return Math.floor(e.length / 2) === n ? t.labels : void 0;
                })(t, r, a)
              : e.props.labels,
            v = e.props.name || "".concat(u, "-").concat(s, "-").concat(a);
          return o.cloneElement(
            e,
            p()(
              {
                labels: h,
                style: d,
                key: "".concat(v, "-key-").concat(a),
                name: v,
                data: U(t, r[a], f),
                colorScale: z(t, e),
                labelComponent: i || e.props.labelComponent,
                xOffset: f,
              },
              l,
            ),
          );
        });
      }
      function q(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function H(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? q(Object(n), !0).forEach(function (e) {
                V(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : q(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function V(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      var $ = { width: 450, height: 300, padding: 50, offset: 0 },
        Y = function (t) {
          var e = null === K || void 0 === K ? void 0 : K.role,
            n = v.h(),
            r = n.getAnimationProps,
            a = n.setAnimationState,
            i = (0, n.getProps)(t),
            c = y.TY(i, $, e),
            u = c.eventKey,
            f = c.containerComponent,
            d = c.standalone,
            h = c.groupComponent,
            x = c.externalEventMutations,
            O = c.width,
            w = c.height,
            S = c.theme,
            A = c.polar,
            j = c.horizontal,
            k = c.name,
            P = o.Children.toArray(c.children),
            E = N(c),
            M = E.domain,
            T = E.scale,
            _ = E.style,
            L = E.origin,
            D = o.useMemo(
              function () {
                return B(i, P, E).map(function (t, e) {
                  var n = p()({ animate: r(i, t, e) }, t.props);
                  return o.cloneElement(t, n);
                });
              },
              [i, P, E, r],
            ),
            I = o.useMemo(
              function () {
                return d
                  ? {
                      domain: M,
                      scale: T,
                      width: O,
                      height: w,
                      standalone: d,
                      theme: S,
                      style: _.parent,
                      horizontal: j,
                      polar: A,
                      origin: L,
                      name: k,
                    }
                  : {};
              },
              [d, M, T, O, w, S, _, j, A, L, k],
            ),
            R = o.useMemo(
              function () {
                return m.I(t);
              },
              [t],
            ),
            W = o.useMemo(
              function () {
                if (d) {
                  var t = s()({}, f.props, I, R);
                  return o.cloneElement(f, t);
                }
                return o.cloneElement(h, R);
              },
              [h, d, f, I, R],
            ),
            F = o.useMemo(
              function () {
                return g.IP(i);
              },
              [i],
            ),
            z = b.Y(t);
          return (
            o.useEffect(
              function () {
                return function () {
                  t.animate && a(z, i);
                };
              },
              [a, z, t, i],
            ),
            l()(F)
              ? o.cloneElement(W, W.props, D)
              : o.createElement(
                  C.Z,
                  {
                    container: W,
                    eventKey: u,
                    events: F,
                    externalEventMutations: x,
                  },
                  D,
                )
          );
        };
      (Y.propTypes = H(
        H(H({}, x.l.baseProps), x.l.dataProps),
        {},
        {
          children: h().oneOfType([h().arrayOf(h().node), h().node]),
          horizontal: h().bool,
          offset: h().number,
        },
      )),
        (Y.defaultProps = {
          containerComponent: o.createElement(O._, null),
          groupComponent: o.createElement("g", null),
          samples: 50,
          sortOrder: "ascending",
          standalone: !0,
          theme: w.J.grayscale,
        });
      var Z = {
          role: "group",
          expectedComponents: [
            "groupComponent",
            "containerComponent",
            "labelComponent",
          ],
          getChildren: B,
        },
        K = Object.assign(o.memo(Y, k()), Z);
      K.displayName = "VictoryGroup";
      var G = n(50235),
        X = n(70219),
        Q = n(10859),
        J = n(79674);
      const tt = (t) => {
        var {
            ariaDesc: e,
            ariaTitle: n,
            children: a,
            colorScale: i,
            containerComponent: c = o.createElement(G.B, null),
            hasPatterns: l,
            patternScale: u,
            themeColor: s,
            theme: f = (0, J.gh)(s),
          } = t,
          p = (0, r.__rest)(t, [
            "ariaDesc",
            "ariaTitle",
            "children",
            "colorScale",
            "containerComponent",
            "hasPatterns",
            "patternScale",
            "themeColor",
            "theme",
          ]);
        const d = o.cloneElement(
            c,
            Object.assign(
              Object.assign({ desc: e, title: n, theme: f }, c.props),
              { className: (0, X.g)({ className: c.props.className }) },
            ),
          ),
          {
            defaultColorScale: h,
            defaultPatternScale: v,
            isPatternDefs: y,
            patternId: m,
          } = (0, Q.cA)({
            colorScale: i,
            hasPatterns: l,
            patternScale: u,
            themeColorScale: f.group.colorScale,
          });
        return o.createElement(
          K,
          Object.assign({ colorScale: i, containerComponent: d, theme: f }, p),
          (0, Q.im)({ children: a, patternScale: v }),
          y && (0, Q.LF)({ patternId: m, colorScale: h }),
        );
      };
      (tt.displayName = "ChartGroup"), i()(tt, K);
    },
    77534: (t, e, n) => {
      "use strict";
      n.d(e, { D: () => f });
      var r = n(75971),
        o = n(72791),
        a = n(62110),
        i = n.n(a),
        c = n(66933),
        l = n.n(c),
        u = n(83485),
        s = n(98278);
      const f = (t) => {
        var { style: e, textAnchor: n } = t,
          a = (0, r.__rest)(t, ["style", "textAnchor"]);
        const i = (t) =>
            l()(Object.assign(Object.assign({}, t), { textAnchor: n }), {
              fill: s.cV.label.fill,
              fontFamily: s.cV.label.fontFamily,
              fontSize: s.cV.label.fontSize,
              letterSpacing: s.cV.label.letterSpacing,
            }),
          c = Array.isArray(e) ? e.map(i) : i(e);
        return o.createElement(
          u.X,
          Object.assign({ style: c, textAnchor: n }, a),
        );
      };
      (f.displayName = "ChartLabel"), i()(f, u.X);
    },
    98278: (t, e, n) => {
      "use strict";
      n.d(e, { cV: () => p });
      var r = n(35684),
        o = n(67690);
      const a = {
        name: "--pf-v5-chart-global--label--Margin",
        value: 8,
        var: "var(--pf-v5-chart-global--label--Margin, 8)",
      };
      var i = n(85134),
        c = n(18769),
        l = n(18425);
      const u = {
          name: "--pf-v5-chart-legend--position",
          value: "right",
          var: "var(--pf-v5-chart-legend--position, right)",
        },
        s = r.Z.var,
        f = c.Z.var,
        p = {
          label: {
            fontFamily: s,
            fontSize: o.Z.value,
            letterSpacing: f,
            margin: a.value,
            fill: i.Z.var,
          },
          legend: { margin: l.Z.value, position: u.value },
        };
    },
    87296: (t, e, n) => {
      "use strict";
      n.d(e, { n: () => r });
      const r = {
        blue: "blue",
        cyan: "cyan",
        default: "blue",
        gold: "gold",
        gray: "gray",
        green: "green",
        multi: "multi",
        multiOrdered: "multi-ordered",
        multiUnordered: "multi-unordered",
        orange: "orange",
        purple: "purple",
      };
    },
    40005: (t, e, n) => {
      "use strict";
      n.d(e, { fm: () => ne, kJ: () => re });
      const r = {
          name: "--pf-v5-chart-axis--tick--stroke--Color",
          value: "#d2d2d2",
          var: "var(--pf-v5-chart-axis--tick--stroke--Color, #d2d2d2)",
        },
        o = {
          axis: {
            style: {
              grid: {
                stroke: {
                  name: "--pf-v5-chart-axis--grid--stroke--Color",
                  value: "#d2d2d2",
                  var: "var(--pf-v5-chart-axis--grid--stroke--Color, #d2d2d2)",
                }.var,
              },
              ticks: { stroke: r.var },
            },
          },
        };
      var a = n(35684),
        i = n(18769),
        c = n(67690);
      const l = {
          name: "--pf-v5-chart-global--label--Padding",
          value: 10,
          var: "var(--pf-v5-chart-global--label--Padding, 10)",
        },
        u = {
          name: "--pf-v5-chart-global--label--stroke",
          value: "transparent",
          var: "var(--pf-v5-chart-global--label--stroke, transparent)",
        },
        s = {
          name: "--pf-v5-chart-global--label--text-anchor",
          value: "middle",
          var: "var(--pf-v5-chart-global--label--text-anchor, middle)",
        };
      var f = n(85134);
      const p = {
          name: "--pf-v5-chart-global--layout--Padding",
          value: 50,
          var: "var(--pf-v5-chart-global--layout--Padding, 50)",
        },
        d = {
          name: "--pf-v5-chart-global--layout--Height",
          value: 300,
          var: "var(--pf-v5-chart-global--layout--Height, 300)",
        },
        h = {
          name: "--pf-v5-chart-global--layout--Width",
          value: 450,
          var: "var(--pf-v5-chart-global--layout--Width, 450)",
        },
        v = {
          name: "--pf-v5-chart-global--stroke-line-cap",
          value: "round",
          var: "var(--pf-v5-chart-global--stroke-line-cap, round)",
        },
        y = {
          name: "--pf-v5-chart-global--stroke-line-join",
          value: "round",
          var: "var(--pf-v5-chart-global--stroke-line-join, round)",
        },
        m = {
          name: "--pf-v5-chart-area--data--Fill",
          value: "#151515",
          var: "var(--pf-v5-chart-area--data--Fill, #151515)",
        },
        g = {
          name: "--pf-v5-chart-area--Opacity",
          value: 0.3,
          var: "var(--pf-v5-chart-area--Opacity, 0.3)",
        },
        b = {
          name: "--pf-v5-chart-area--stroke--Width",
          value: 2,
          var: "var(--pf-v5-chart-area--stroke--Width, 2)",
        },
        x = {
          name: "--pf-v5-chart-axis--axis--stroke--Width",
          value: 1,
          var: "var(--pf-v5-chart-axis--axis--stroke--Width, 1)",
        },
        O = {
          name: "--pf-v5-chart-axis--axis--stroke--Color",
          value: "#d2d2d2",
          var: "var(--pf-v5-chart-axis--axis--stroke--Color, #d2d2d2)",
        },
        w = {
          name: "--pf-v5-chart-axis--axis--Fill",
          value: "transparent",
          var: "var(--pf-v5-chart-axis--axis--Fill, transparent)",
        },
        C = {
          name: "--pf-v5-chart-axis--axis-label--Padding",
          value: 40,
          var: "var(--pf-v5-chart-axis--axis-label--Padding, 40)",
        },
        S = {
          name: "--pf-v5-chart-axis--axis-label--stroke--Color",
          value: "transparent",
          var: "var(--pf-v5-chart-axis--axis-label--stroke--Color, transparent)",
        },
        A = {
          name: "--pf-v5-chart-axis--grid--Fill",
          value: "none",
          var: "var(--pf-v5-chart-axis--grid--Fill, none)",
        },
        j = {
          name: "--pf-v5-chart-axis--grid--PointerEvents",
          value: "painted",
          var: "var(--pf-v5-chart-axis--grid--PointerEvents, painted)",
        },
        k = {
          name: "--pf-v5-chart-axis--tick--Fill",
          value: "transparent",
          var: "var(--pf-v5-chart-axis--tick--Fill, transparent)",
        },
        P = {
          name: "--pf-v5-chart-axis--tick--Size",
          value: 5,
          var: "var(--pf-v5-chart-axis--tick--Size, 5)",
        },
        E = {
          name: "--pf-v5-chart-axis--tick--Width",
          value: 1,
          var: "var(--pf-v5-chart-axis--tick--Width, 1)",
        },
        M = {
          name: "--pf-v5-chart-axis--tick-label--Fill",
          value: "#4f5255",
          var: "var(--pf-v5-chart-axis--tick-label--Fill, #4f5255)",
        },
        T = {
          name: "--pf-v5-chart-bar--Width",
          value: 10,
          var: "var(--pf-v5-chart-bar--Width, 10)",
        },
        _ = {
          name: "--pf-v5-chart-bar--data--stroke",
          value: "none",
          var: "var(--pf-v5-chart-bar--data--stroke, none)",
        },
        L = {
          name: "--pf-v5-chart-bar--data--Fill",
          value: "#151515",
          var: "var(--pf-v5-chart-bar--data--Fill, #151515)",
        },
        D = {
          name: "--pf-v5-chart-bar--data--Padding",
          value: 8,
          var: "var(--pf-v5-chart-bar--data--Padding, 8)",
        },
        I = {
          name: "--pf-v5-chart-bar--data-stroke--Width",
          value: 0,
          var: "var(--pf-v5-chart-bar--data-stroke--Width, 0)",
        },
        R = {
          name: "--pf-v5-chart-boxplot--max--Padding",
          value: 8,
          var: "var(--pf-v5-chart-boxplot--max--Padding, 8)",
        },
        N = {
          name: "--pf-v5-chart-boxplot--max--stroke--Color",
          value: "#151515",
          var: "var(--pf-v5-chart-boxplot--max--stroke--Color, #151515)",
        },
        W = {
          name: "--pf-v5-chart-boxplot--max--stroke--Width",
          value: 1,
          var: "var(--pf-v5-chart-boxplot--max--stroke--Width, 1)",
        },
        F = {
          name: "--pf-v5-chart-boxplot--median--Padding",
          value: 8,
          var: "var(--pf-v5-chart-boxplot--median--Padding, 8)",
        },
        z = {
          name: "--pf-v5-chart-boxplot--median--stroke--Color",
          value: "#151515",
          var: "var(--pf-v5-chart-boxplot--median--stroke--Color, #151515)",
        },
        U = {
          name: "--pf-v5-chart-boxplot--median--stroke--Width",
          value: 1,
          var: "var(--pf-v5-chart-boxplot--median--stroke--Width, 1)",
        },
        B = {
          name: "--pf-v5-chart-boxplot--min--Padding",
          value: 8,
          var: "var(--pf-v5-chart-boxplot--min--Padding, 8)",
        },
        q = {
          name: "--pf-v5-chart-boxplot--min--stroke--Width",
          value: 1,
          var: "var(--pf-v5-chart-boxplot--min--stroke--Width, 1)",
        },
        H = {
          name: "--pf-v5-chart-boxplot--min--stroke--Color",
          value: "#151515",
          var: "var(--pf-v5-chart-boxplot--min--stroke--Color, #151515)",
        },
        V = {
          name: "--pf-v5-chart-boxplot--lower-quartile--Padding",
          value: 8,
          var: "var(--pf-v5-chart-boxplot--lower-quartile--Padding, 8)",
        },
        $ = {
          name: "--pf-v5-chart-boxplot--lower-quartile--Fill",
          value: "#8a8d90",
          var: "var(--pf-v5-chart-boxplot--lower-quartile--Fill, #8a8d90)",
        },
        Y = {
          name: "--pf-v5-chart-boxplot--upper-quartile--Padding",
          value: 8,
          var: "var(--pf-v5-chart-boxplot--upper-quartile--Padding, 8)",
        },
        Z = {
          name: "--pf-v5-chart-boxplot--upper-quartile--Fill",
          value: "#8a8d90",
          var: "var(--pf-v5-chart-boxplot--upper-quartile--Fill, #8a8d90)",
        },
        K = {
          name: "--pf-v5-chart-boxplot--box--Width",
          value: 20,
          var: "var(--pf-v5-chart-boxplot--box--Width, 20)",
        },
        G = {
          name: "--pf-v5-chart-candelstick--data--stroke--Width",
          value: 1,
          var: "var(--pf-v5-chart-candelstick--data--stroke--Width, 1)",
        },
        X = {
          name: "--pf-v5-chart-candelstick--data--stroke--Color",
          value: "#151515",
          var: "var(--pf-v5-chart-candelstick--data--stroke--Color, #151515)",
        },
        Q = {
          name: "--pf-v5-chart-candelstick--candle--positive--Color",
          value: "#fff",
          var: "var(--pf-v5-chart-candelstick--candle--positive--Color, #fff)",
        },
        J = {
          name: "--pf-v5-chart-candelstick--candle--negative--Color",
          value: "#151515",
          var: "var(--pf-v5-chart-candelstick--candle--negative--Color, #151515)",
        },
        tt = {
          name: "--pf-v5-chart-errorbar--BorderWidth",
          value: 8,
          var: "var(--pf-v5-chart-errorbar--BorderWidth, 8)",
        },
        et = {
          name: "--pf-v5-chart-errorbar--data--Fill",
          value: "transparent",
          var: "var(--pf-v5-chart-errorbar--data--Fill, transparent)",
        },
        nt = {
          name: "--pf-v5-chart-errorbar--data--Opacity",
          value: 1,
          var: "var(--pf-v5-chart-errorbar--data--Opacity, 1)",
        },
        rt = {
          name: "--pf-v5-chart-errorbar--data-stroke--Width",
          value: 2,
          var: "var(--pf-v5-chart-errorbar--data-stroke--Width, 2)",
        },
        ot = {
          name: "--pf-v5-chart-errorbar--data-stroke--Color",
          value: "#151515",
          var: "var(--pf-v5-chart-errorbar--data-stroke--Color, #151515)",
        },
        at = {
          name: "--pf-v5-chart-legend--gutter--Width",
          value: 20,
          var: "var(--pf-v5-chart-legend--gutter--Width, 20)",
        },
        it = {
          name: "--pf-v5-chart-legend--orientation",
          value: "horizontal",
          var: "var(--pf-v5-chart-legend--orientation, horizontal)",
        },
        ct = {
          name: "--pf-v5-chart-legend--title--orientation",
          value: "top",
          var: "var(--pf-v5-chart-legend--title--orientation, top)",
        },
        lt = {
          name: "--pf-v5-chart-legend--data--type",
          value: "square",
          var: "var(--pf-v5-chart-legend--data--type, square)",
        },
        ut = {
          name: "--pf-v5-chart-legend--title--Padding",
          value: 2,
          var: "var(--pf-v5-chart-legend--title--Padding, 2)",
        },
        st = {
          name: "--pf-v5-chart-line--data--Fill",
          value: "transparent",
          var: "var(--pf-v5-chart-line--data--Fill, transparent)",
        },
        ft = {
          name: "--pf-v5-chart-line--data--Opacity",
          value: 1,
          var: "var(--pf-v5-chart-line--data--Opacity, 1)",
        },
        pt = {
          name: "--pf-v5-chart-line--data--stroke--Width",
          value: 2,
          var: "var(--pf-v5-chart-line--data--stroke--Width, 2)",
        },
        dt = {
          name: "--pf-v5-chart-line--data--stroke--Color",
          value: "#151515",
          var: "var(--pf-v5-chart-line--data--stroke--Color, #151515)",
        },
        ht = {
          name: "--pf-v5-chart-pie--Padding",
          value: 20,
          var: "var(--pf-v5-chart-pie--Padding, 20)",
        },
        vt = {
          name: "--pf-v5-chart-pie--data--Padding",
          value: 8,
          var: "var(--pf-v5-chart-pie--data--Padding, 8)",
        },
        yt = {
          name: "--pf-v5-chart-pie--data--stroke--Width",
          value: 1,
          var: "var(--pf-v5-chart-pie--data--stroke--Width, 1)",
        },
        mt = {
          name: "--pf-v5-chart-pie--data--stroke--Color",
          value: "transparent",
          var: "var(--pf-v5-chart-pie--data--stroke--Color, transparent)",
        },
        gt = {
          name: "--pf-v5-chart-pie--labels--Padding",
          value: 8,
          var: "var(--pf-v5-chart-pie--labels--Padding, 8)",
        },
        bt = {
          name: "--pf-v5-chart-pie--Height",
          value: 230,
          var: "var(--pf-v5-chart-pie--Height, 230)",
        },
        xt = {
          name: "--pf-v5-chart-pie--Width",
          value: 230,
          var: "var(--pf-v5-chart-pie--Width, 230)",
        },
        Ot = {
          name: "--pf-v5-chart-scatter--data--stroke--Color",
          value: "transparent",
          var: "var(--pf-v5-chart-scatter--data--stroke--Color, transparent)",
        },
        wt = {
          name: "--pf-v5-chart-scatter--data--stroke--Width",
          value: 0,
          var: "var(--pf-v5-chart-scatter--data--stroke--Width, 0)",
        },
        Ct = {
          name: "--pf-v5-chart-scatter--data--Opacity",
          value: 1,
          var: "var(--pf-v5-chart-scatter--data--Opacity, 1)",
        },
        St = {
          name: "--pf-v5-chart-scatter--data--Fill",
          value: "#151515",
          var: "var(--pf-v5-chart-scatter--data--Fill, #151515)",
        },
        At = {
          name: "--pf-v5-chart-stack--data--stroke--Width",
          value: 1,
          var: "var(--pf-v5-chart-stack--data--stroke--Width, 1)",
        },
        jt = {
          name: "--pf-v5-chart-tooltip--corner-radius",
          value: 0,
          var: "var(--pf-v5-chart-tooltip--corner-radius, 0)",
        },
        kt = {
          name: "--pf-v5-chart-tooltip--pointer-length",
          value: 10,
          var: "var(--pf-v5-chart-tooltip--pointer-length, 10)",
        },
        Pt = {
          name: "--pf-v5-chart-tooltip--Fill",
          value: "#f0f0f0",
          var: "var(--pf-v5-chart-tooltip--Fill, #f0f0f0)",
        },
        Et = {
          name: "--pf-v5-chart-tooltip--flyoutStyle--corner-radius",
          value: 0,
          var: "var(--pf-v5-chart-tooltip--flyoutStyle--corner-radius, 0)",
        },
        Mt = {
          name: "--pf-v5-chart-tooltip--flyoutStyle--stroke--Width",
          value: 0,
          var: "var(--pf-v5-chart-tooltip--flyoutStyle--stroke--Width, 0)",
        },
        Tt = {
          name: "--pf-v5-chart-tooltip--flyoutStyle--PointerEvents",
          value: "none",
          var: "var(--pf-v5-chart-tooltip--flyoutStyle--PointerEvents, none)",
        },
        _t = {
          name: "--pf-v5-chart-tooltip--flyoutStyle--stroke--Color",
          value: "#151515",
          var: "var(--pf-v5-chart-tooltip--flyoutStyle--stroke--Color, #151515)",
        },
        Lt = {
          name: "--pf-v5-chart-tooltip--flyoutStyle--Fill",
          value: "#151515",
          var: "var(--pf-v5-chart-tooltip--flyoutStyle--Fill, #151515)",
        },
        Dt = {
          name: "--pf-v5-chart-tooltip--pointer--Width",
          value: 20,
          var: "var(--pf-v5-chart-tooltip--pointer--Width, 20)",
        },
        It = {
          name: "--pf-v5-chart-tooltip--Padding",
          value: 8,
          var: "var(--pf-v5-chart-tooltip--Padding, 8)",
        },
        Rt = {
          name: "--pf-v5-chart-tooltip--PointerEvents",
          value: "none",
          var: "var(--pf-v5-chart-tooltip--PointerEvents, none)",
        },
        Nt = {
          name: "--pf-v5-chart-voronoi--data--Fill",
          value: "transparent",
          var: "var(--pf-v5-chart-voronoi--data--Fill, transparent)",
        },
        Wt = {
          name: "--pf-v5-chart-voronoi--data--stroke--Color",
          value: "transparent",
          var: "var(--pf-v5-chart-voronoi--data--stroke--Color, transparent)",
        },
        Ft = {
          name: "--pf-v5-chart-voronoi--data--stroke--Width",
          value: 0,
          var: "var(--pf-v5-chart-voronoi--data--stroke--Width, 0)",
        },
        zt = {
          name: "--pf-v5-chart-voronoi--labels--Fill",
          value: "#f0f0f0",
          var: "var(--pf-v5-chart-voronoi--labels--Fill, #f0f0f0)",
        },
        Ut = {
          name: "--pf-v5-chart-voronoi--labels--Padding",
          value: 8,
          var: "var(--pf-v5-chart-voronoi--labels--Padding, 8)",
        },
        Bt = {
          name: "--pf-v5-chart-voronoi--labels--PointerEvents",
          value: "none",
          var: "var(--pf-v5-chart-voronoi--labels--PointerEvents, none)",
        },
        qt = {
          name: "--pf-v5-chart-voronoi--flyout--stroke--Width",
          value: 1,
          var: "var(--pf-v5-chart-voronoi--flyout--stroke--Width, 1)",
        },
        Ht = {
          name: "--pf-v5-chart-voronoi--flyout--PointerEvents",
          value: "none",
          var: "var(--pf-v5-chart-voronoi--flyout--PointerEvents, none)",
        },
        Vt = {
          name: "--pf-v5-chart-voronoi--flyout--stroke--Color",
          value: "#151515",
          var: "var(--pf-v5-chart-voronoi--flyout--stroke--Color, #151515)",
        },
        $t = {
          name: "--pf-v5-chart-voronoi--flyout--stroke--Fill",
          value: "#151515",
          var: "var(--pf-v5-chart-voronoi--flyout--stroke--Fill, #151515)",
        },
        Yt = a.Z.value.replace(/ /g, ""),
        Zt = i.Z.value,
        Kt = c.Z.value,
        Gt = {
          fontFamily: Yt,
          fontSize: Kt,
          letterSpacing: Zt,
          padding: l.value,
          stroke: u.var,
          fill: f.Z.var,
        },
        Xt = Object.assign(Object.assign({}, Gt), { textAnchor: s.value }),
        Qt = { padding: p.value, height: d.value, width: h.value },
        Jt = v.value,
        te = y.value,
        ee = {
          area: Object.assign(Object.assign({}, Qt), {
            style: {
              data: { fill: m.var, fillOpacity: g.value, strokeWidth: b.value },
              labels: Xt,
            },
          }),
          axis: Object.assign(Object.assign({}, Qt), {
            style: {
              axis: {
                fill: w.var,
                strokeWidth: x.value,
                stroke: O.var,
                strokeLinecap: Jt,
                strokeLinejoin: te,
              },
              axisLabel: Object.assign(Object.assign({}, Xt), {
                padding: C.value,
                stroke: S.var,
              }),
              grid: {
                fill: A.var,
                stroke: "none",
                pointerEvents: j.value,
                strokeLinecap: Jt,
                strokeLinejoin: te,
              },
              ticks: {
                fill: k.var,
                size: P.value,
                stroke: r.var,
                strokeLinecap: Jt,
                strokeLinejoin: te,
                strokeWidth: E.value,
              },
              tickLabels: Object.assign(Object.assign({}, Gt), { fill: M.var }),
            },
          }),
          bar: Object.assign(Object.assign({}, Qt), {
            barWidth: T.value,
            style: {
              data: {
                fill: L.var,
                padding: D.value,
                stroke: _.var,
                strokeWidth: I.value,
              },
              labels: Gt,
            },
          }),
          boxplot: Object.assign(Object.assign({}, Qt), {
            style: {
              max: { padding: R.value, stroke: N.var, strokeWidth: W.value },
              maxLabels: Gt,
              median: { padding: F.value, stroke: z.var, strokeWidth: U.value },
              medianLabels: Gt,
              min: { padding: B.value, stroke: H.var, strokeWidth: q.value },
              minLabels: Gt,
              q1: { fill: $.var, padding: V.value },
              q1Labels: Gt,
              q3: { fill: Z.var, padding: Y.value },
              q3Labels: Gt,
            },
            boxWidth: K.value,
          }),
          candlestick: Object.assign(Object.assign({}, Qt), {
            candleColors: { positive: Q.var, negative: J.var },
            style: {
              data: { stroke: X.var, strokeWidth: G.value },
              labels: Xt,
            },
          }),
          chart: Object.assign({}, Qt),
          errorbar: Object.assign(Object.assign({}, Qt), {
            borderWidth: tt.value,
            style: {
              data: {
                fill: et.var,
                opacity: nt.value,
                stroke: ot.var,
                strokeWidth: rt.value,
              },
              labels: Xt,
            },
          }),
          group: Object.assign({}, Qt),
          legend: {
            gutter: at.value,
            orientation: it.value,
            titleOrientation: ct.value,
            style: {
              data: { type: lt.value },
              labels: Gt,
              title: Object.assign(Object.assign({}, Gt), {
                fontSize: Kt,
                padding: ut.value,
              }),
            },
          },
          line: Object.assign(Object.assign({}, Qt), {
            style: {
              data: {
                fill: st.var,
                opacity: ft.value,
                stroke: dt.var,
                strokeWidth: pt.value,
              },
              labels: Xt,
            },
          }),
          pie: {
            padding: ht.value,
            style: {
              data: {
                padding: vt.value,
                stroke: mt.var,
                strokeWidth: yt.value,
              },
              labels: Object.assign(Object.assign({}, Gt), {
                padding: gt.value,
              }),
            },
            height: bt.value,
            width: xt.value,
          },
          scatter: Object.assign(Object.assign({}, Qt), {
            style: {
              data: {
                fill: St.var,
                opacity: Ct.value,
                stroke: Ot.var,
                strokeWidth: wt.value,
              },
              labels: Xt,
            },
          }),
          stack: Object.assign(Object.assign({}, Qt), {
            style: { data: { strokeWidth: At.value } },
          }),
          tooltip: {
            cornerRadius: jt.value,
            flyoutPadding: It.value,
            flyoutStyle: {
              cornerRadius: Et.value,
              fill: Lt.var,
              pointerEvents: Tt.var,
              stroke: _t.var,
              strokeWidth: Mt.var,
            },
            pointerLength: kt.value,
            pointerWidth: Dt.value,
            style: { fill: Pt.var, pointerEvents: Rt.var },
          },
          voronoi: Object.assign(Object.assign({}, Qt), {
            style: {
              data: { fill: Nt.var, stroke: Wt.var, strokeWidth: Ft.value },
              labels: Object.assign(Object.assign({}, Xt), {
                fill: zt.var,
                padding: Ut.value,
                pointerEvents: Bt.value,
              }),
              flyout: {
                fill: $t.var,
                pointerEvents: Ht.var,
                stroke: Vt.var,
                strokeWidth: qt.var,
              },
            },
          }),
        },
        ne = o,
        re = ee;
    },
    3782: (t, e, n) => {
      "use strict";
      n.d(e, { h: () => V });
      var r = n(75971),
        o = n(72791),
        a = n(62110),
        i = n.n(a),
        c = n(45812),
        l = n.n(c),
        u = n(93977),
        s = n.n(u),
        f = n(30804),
        p = n.n(f),
        d = n(66933),
        h = n.n(d),
        v = n(15687),
        y = n.n(v),
        m = n(52007),
        g = n.n(m),
        b = n(21222),
        x = n(58853),
        O = n(8091),
        w = n(62795),
        C = n(41913),
        S = n(42745),
        A = n(83485),
        j = n(97409),
        k = n(46577),
        P = n(42017);
      function E(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function M(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? E(Object(n), !0).forEach(function (e) {
                T(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : E(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function T(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      var _ = function (t) {
          var e = t.orientation || "top";
          return "left" === e || "right" === e
            ? (function (t) {
                var e = t.pointerWidth,
                  n = t.cornerRadius,
                  r = t.orientation,
                  o = t.width,
                  a = t.height,
                  i = t.center,
                  c = "left" === r ? 1 : -1,
                  l = t.x + (t.dx || 0),
                  u = t.y + (t.dy || 0),
                  f = s()(i) && i.x,
                  p = s()(i) && i.y,
                  d = f - c * (o / 2),
                  h = f + c * (o / 2),
                  v = p + a / 2,
                  y = p - a / 2,
                  m = c * (l - d) > 0 ? 0 : t.pointerLength,
                  g = "left" === r ? "0 0 0" : "0 0 1",
                  b = "".concat(n, " ").concat(n, " ").concat(g);
                return "M "
                  .concat(d, ", ")
                  .concat(p - e / 2, "\n    L ")
                  .concat(m ? l : d, ", ")
                  .concat(m ? u : p + e / 2, "\n    L ")
                  .concat(d, ", ")
                  .concat(p + e / 2, "\n    L ")
                  .concat(d, ", ")
                  .concat(v - n, "\n    A ")
                  .concat(b, " ")
                  .concat(d + c * n, ", ")
                  .concat(v, "\n    L ")
                  .concat(h - c * n, ", ")
                  .concat(v, "\n    A ")
                  .concat(b, " ")
                  .concat(h, ", ")
                  .concat(v - n, "\n    L ")
                  .concat(h, ", ")
                  .concat(y + n, "\n    A ")
                  .concat(b, " ")
                  .concat(h - c * n, ", ")
                  .concat(y, "\n    L ")
                  .concat(d + c * n, ", ")
                  .concat(y, "\n    A ")
                  .concat(b, " ")
                  .concat(d, ", ")
                  .concat(y + n, "\n    z");
              })(t)
            : (function (t) {
                var e = t.pointerWidth,
                  n = t.cornerRadius,
                  r = t.orientation,
                  o = t.width,
                  a = t.height,
                  i = t.center,
                  c = "bottom" === r ? 1 : -1,
                  l = t.x + (t.dx || 0),
                  u = t.y + (t.dy || 0),
                  f = s()(i) && i.x,
                  p = s()(i) && i.y,
                  d = p + c * (a / 2),
                  h = p - c * (a / 2),
                  v = f + o / 2,
                  y = f - o / 2,
                  m = c * (u - d) < 0 ? 0 : t.pointerLength,
                  g = "bottom" === r ? "0 0 0" : "0 0 1",
                  b = "".concat(n, " ").concat(n, " ").concat(g);
                return "M "
                  .concat(f - e / 2, ", ")
                  .concat(d, "\n    L ")
                  .concat(m ? l : f + e / 2, ", ")
                  .concat(m ? u : d, "\n    L ")
                  .concat(f + e / 2, ", ")
                  .concat(d, "\n    L ")
                  .concat(v - n, ", ")
                  .concat(d, "\n    A ")
                  .concat(b, " ")
                  .concat(v, ", ")
                  .concat(d - c * n, "\n    L ")
                  .concat(v, ", ")
                  .concat(h + c * n, "\n    A ")
                  .concat(b, " ")
                  .concat(v - n, ", ")
                  .concat(h, "\n    L ")
                  .concat(y + n, ", ")
                  .concat(h, "\n    A ")
                  .concat(b, " ")
                  .concat(y, ", ")
                  .concat(h + c * n, "\n    L ")
                  .concat(y, ", ")
                  .concat(d - c * n, "\n    A ")
                  .concat(b, " ")
                  .concat(y + n, ", ")
                  .concat(d, "\n    z");
              })(t);
        },
        L = function (t) {
          t = (function (t) {
            var e = O.xs(t.id, t),
              n = O.F3(t.style, t);
            return y()({}, t, { id: e, style: n });
          })(t);
          var e = j.I(t);
          return o.cloneElement(
            t.pathComponent,
            M(
              M(M({}, t.events), e),
              {},
              {
                style: t.style,
                d: _(t),
                className: t.className,
                shapeRendering: t.shapeRendering,
                role: t.role,
                transform: t.transform,
                clipPath: t.clipPath,
              },
            ),
          );
        };
      (L.propTypes = M(
        M({}, k.l.primitiveProps),
        {},
        {
          center: g().shape({ x: g().number, y: g().number }),
          cornerRadius: g().number,
          datum: g().object,
          dx: g().number,
          dy: g().number,
          height: g().number,
          orientation: g().oneOf(["top", "bottom", "left", "right"]),
          pathComponent: g().element,
          pointerLength: g().number,
          pointerWidth: g().number,
          width: g().number,
          x: g().number,
          y: g().number,
        },
      )),
        (L.defaultProps = {
          pathComponent: o.createElement(P.y, null),
          role: "presentation",
          shapeRendering: "auto",
        });
      const D = L;
      function I(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return R(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return R(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return R(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function R(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function N(t, e) {
        for (var n = 0; n < e.length; n++) {
          var r = e[n];
          (r.enumerable = r.enumerable || !1),
            (r.configurable = !0),
            "value" in r && (r.writable = !0),
            Object.defineProperty(t, r.key, r);
        }
      }
      function W(t, e) {
        return (
          (W = Object.setPrototypeOf
            ? Object.setPrototypeOf.bind()
            : function (t, e) {
                return (t.__proto__ = e), t;
              }),
          W(t, e)
        );
      }
      function F(t) {
        var e = (function () {
          if ("undefined" === typeof Reflect || !Reflect.construct) return !1;
          if (Reflect.construct.sham) return !1;
          if ("function" === typeof Proxy) return !0;
          try {
            return (
              Boolean.prototype.valueOf.call(
                Reflect.construct(Boolean, [], function () {}),
              ),
              !0
            );
          } catch (t) {
            return !1;
          }
        })();
        return function () {
          var n,
            r = z(t);
          if (e) {
            var o = z(this).constructor;
            n = Reflect.construct(r, arguments, o);
          } else n = r.apply(this, arguments);
          return (function (t, e) {
            if (e && ("object" === typeof e || "function" === typeof e))
              return e;
            if (void 0 !== e)
              throw new TypeError(
                "Derived constructors may only return object or undefined",
              );
            return (function (t) {
              if (void 0 === t)
                throw new ReferenceError(
                  "this hasn't been initialised - super() hasn't been called",
                );
              return t;
            })(t);
          })(this, n);
        };
      }
      function z(t) {
        return (
          (z = Object.setPrototypeOf
            ? Object.getPrototypeOf.bind()
            : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t);
              }),
          z(t)
        );
      }
      var U = { cornerRadius: 5, pointerLength: 10, pointerWidth: 10 },
        B = (function (t) {
          !(function (t, e) {
            if ("function" !== typeof e && null !== e)
              throw new TypeError(
                "Super expression must either be null or a function",
              );
            (t.prototype = Object.create(e && e.prototype, {
              constructor: { value: t, writable: !0, configurable: !0 },
            })),
              Object.defineProperty(t, "prototype", { writable: !1 }),
              e && W(t, e);
          })(i, t);
          var e,
            n,
            r,
            a = F(i);
          function i(t) {
            var e;
            return (
              (function (t, e) {
                if (!(t instanceof e))
                  throw new TypeError("Cannot call a class as a function");
              })(this, i),
              ((e = a.call(this, t)).id =
                void 0 === t.id ? p()("tooltip-") : t.id),
              e
            );
          }
          return (
            (e = i),
            (n = [
              {
                key: "getDefaultOrientation",
                value: function (t) {
                  var e = t.datum,
                    n = t.horizontal;
                  if (!t.polar) {
                    var r = n ? "right" : "top",
                      o = n ? "left" : "bottom";
                    return e && e.y < 0 ? o : r;
                  }
                  return this.getPolarOrientation(t, e);
                },
              },
              {
                key: "getPolarOrientation",
                value: function (t, e) {
                  var n = b.ow(t, e),
                    r = t.labelPlacement || "vertical";
                  return " vertical" === r
                    ? this.getVerticalOrientations(n)
                    : "parallel" === r
                      ? n < 90 || n > 270
                        ? "right"
                        : "left"
                      : n > 180
                        ? "bottom"
                        : "top";
                },
              },
              {
                key: "getVerticalOrientations",
                value: function (t) {
                  return t < 45 || t > 315
                    ? "right"
                    : t >= 45 && t <= 135
                      ? "top"
                      : t > 135 && t < 225
                        ? "left"
                        : "bottom";
                },
              },
              {
                key: "getStyles",
                value: function (t) {
                  var e = t.theme || x.J.grayscale,
                    n =
                      e && e.tooltip && e.tooltip.style ? e.tooltip.style : {},
                    r = Array.isArray(t.style)
                      ? t.style.map(function (t) {
                          return h()({}, t, n);
                        })
                      : h()({}, t.style, n),
                    o =
                      e && e.tooltip && e.tooltip.flyoutStyle
                        ? e.tooltip.flyoutStyle
                        : {},
                    a = t.flyoutStyle ? h()({}, t.flyoutStyle, o) : o,
                    i = Array.isArray(r)
                      ? r.map(function (e) {
                          return O.F3(e, t);
                        })
                      : O.F3(r, t);
                  return {
                    style: i,
                    flyoutStyle: O.F3(a, y()({}, t, { style: i })),
                  };
                },
              },
              {
                key: "getEvaluatedProps",
                value: function (t) {
                  var e = t.cornerRadius,
                    n = t.centerOffset,
                    r = t.dx,
                    o = t.dy,
                    a = O.xs(t.active, t),
                    i = O.xs(t.text, y()({}, t, { active: a })),
                    c = this.getStyles(y()({}, t, { active: a, text: i })),
                    l = c.style,
                    u = c.flyoutStyle,
                    f =
                      O.xs(
                        t.orientation,
                        y()({}, t, {
                          active: a,
                          text: i,
                          style: l,
                          flyoutStyle: u,
                        }),
                      ) || this.getDefaultOrientation(t),
                    p =
                      O.xs(
                        t.flyoutPadding,
                        y()({}, t, {
                          active: a,
                          text: i,
                          style: l,
                          flyoutStyle: u,
                          orientation: f,
                        }),
                      ) || this.getLabelPadding(l),
                    d = O.tQ({ padding: p }),
                    h = O.xs(
                      t.pointerWidth,
                      y()({}, t, {
                        active: a,
                        text: i,
                        style: l,
                        flyoutStyle: u,
                        orientation: f,
                      }),
                    ),
                    v = O.xs(
                      t.pointerLength,
                      y()({}, t, {
                        active: a,
                        text: i,
                        style: l,
                        flyoutStyle: u,
                        orientation: f,
                      }),
                    ),
                    m = w.Z9(i, l),
                    g = this.getDimensions(
                      y()({}, t, {
                        style: l,
                        flyoutStyle: u,
                        active: a,
                        text: i,
                        orientation: f,
                        flyoutPadding: d,
                        pointerWidth: h,
                        pointerLength: v,
                      }),
                      m,
                    ),
                    b = g.flyoutHeight,
                    x = g.flyoutWidth,
                    C = y()({}, t, {
                      active: a,
                      text: i,
                      style: l,
                      flyoutStyle: u,
                      orientation: f,
                      flyoutHeight: b,
                      flyoutWidth: x,
                      flyoutPadding: d,
                      pointerWidth: h,
                      pointerLength: v,
                    }),
                    S = s()(n) && void 0 !== n.x ? O.xs(n.x, C) : 0,
                    A = s()(n) && void 0 !== n.y ? O.xs(n.y, C) : 0;
                  return y()({}, C, {
                    centerOffset: { x: S, y: A },
                    dx: void 0 !== r ? O.xs(r, C) : 0,
                    dy: void 0 !== o ? O.xs(o, C) : 0,
                    cornerRadius: O.xs(e, C),
                  });
                },
              },
              {
                key: "getCalculatedValues",
                value: function (t) {
                  var e = t.style,
                    n = t.text,
                    r = t.flyoutStyle,
                    o = { height: t.flyoutHeight, width: t.flyoutWidth };
                  return {
                    style: e,
                    flyoutStyle: r,
                    labelSize: w.Z9(n, e),
                    flyoutDimensions: o,
                    flyoutCenter: this.getFlyoutCenter(t, o),
                    transform: this.getTransform(t),
                  };
                },
              },
              {
                key: "getTransform",
                value: function (t) {
                  var e = t.x,
                    n = t.y,
                    r =
                      (t.style || {}).angle ||
                      t.angle ||
                      this.getDefaultAngle(t);
                  return r
                    ? "rotate(".concat(r, " ").concat(e, " ").concat(n, ")")
                    : void 0;
                },
              },
              {
                key: "getDefaultAngle",
                value: function (t) {
                  var e = t.polar,
                    n = t.labelPlacement,
                    r = t.orientation,
                    o = t.datum;
                  if (!e || !n || "vertical" === n) return 0;
                  var a,
                    i = b.ow(t, o);
                  return (
                    0 === i || 180 === i
                      ? (a = "top" === r && 180 === i ? 270 : 90)
                      : i > 0 && i < 180
                        ? (a = 90 - i)
                        : i > 180 && i < 360 && (a = 270 - i),
                    a +
                      ((i > 90 && i < 180) || i > 270 ? 1 : -1) *
                        ("perpendicular" === n ? 0 : 90)
                  );
                },
              },
              {
                key: "constrainTooltip",
                value: function (t, e, n) {
                  var r = t.x,
                    o = t.y,
                    a = n.width,
                    i = n.height,
                    c = [0, e.width],
                    l = [0, e.height],
                    u = [r - a / 2, r + a / 2],
                    s = [o - i / 2, o + i / 2],
                    f = [
                      u[0] < c[0] ? c[0] - u[0] : 0,
                      u[1] > c[1] ? u[1] - c[1] : 0,
                    ],
                    p = [
                      s[0] < l[0] ? l[0] - s[0] : 0,
                      s[1] > l[1] ? s[1] - l[1] : 0,
                    ];
                  return {
                    x: Math.round(r + f[0] - f[1]),
                    y: Math.round(o + p[0] - p[1]),
                  };
                },
              },
              {
                key: "getFlyoutCenter",
                value: function (t, e) {
                  var n = t.x,
                    r = t.y,
                    o = t.dx,
                    a = t.dy,
                    i = t.pointerLength,
                    c = t.orientation,
                    l = t.constrainToVisibleArea,
                    u = t.centerOffset,
                    f = e.height,
                    p = e.width,
                    d = "left" === c ? -1 : 1,
                    h = "bottom" === c ? -1 : 1,
                    v = {
                      x:
                        "left" === c || "right" === c
                          ? n + d * (i + p / 2 + d * o)
                          : n + o,
                      y:
                        "top" === c || "bottom" === c
                          ? r - h * (i + f / 2 - h * a)
                          : r + a,
                    },
                    y =
                      s()(t.center) && void 0 !== t.center.x ? t.center.x : v.x,
                    m =
                      s()(t.center) && void 0 !== t.center.y ? t.center.y : v.y,
                    g = { x: y + u.x, y: m + u.y };
                  return l ? this.constrainTooltip(g, t, e) : g;
                },
              },
              {
                key: "getLabelPadding",
                value: function (t) {
                  if (!t) return 0;
                  var e = Array.isArray(t)
                    ? t.map(function (t) {
                        return t.padding;
                      })
                    : [t.padding];
                  return Math.max.apply(Math, I(e).concat([0]));
                },
              },
              {
                key: "getDimensions",
                value: function (t, e) {
                  var n = t.orientation,
                    r = t.pointerLength,
                    o = t.pointerWidth,
                    a = t.flyoutHeight,
                    i = t.flyoutWidth,
                    c = t.flyoutPadding,
                    l = O.xs(t.cornerRadius, t);
                  return {
                    flyoutHeight: a
                      ? O.xs(a, t)
                      : (function () {
                          var t = e.height + c.top + c.bottom,
                            r =
                              "top" === n || "bottom" === n ? 2 * l : 2 * l + o;
                          return Math.max(r, t);
                        })(),
                    flyoutWidth: i
                      ? O.xs(i, t)
                      : (function () {
                          var t = e.width + c.left + c.right,
                            o =
                              "left" === n || "right" === n ? 2 * l + r : 2 * l;
                          return Math.max(o, t);
                        })(),
                  };
                },
              },
              {
                key: "getLabelProps",
                value: function (t, e) {
                  var n = e.flyoutCenter,
                    r = e.style,
                    o = e.labelSize,
                    a = e.dy,
                    i = void 0 === a ? 0 : a,
                    c = e.dx,
                    l = void 0 === c ? 0 : c,
                    u = t.text,
                    s = t.datum,
                    f = t.activePoints,
                    p = t.labelComponent,
                    d = t.index,
                    v = t.flyoutPadding,
                    y =
                      (Array.isArray(r) && r.length
                        ? r[0].textAnchor
                        : r.textAnchor) || "middle";
                  return h()({}, p.props, {
                    key: "".concat(this.id, "-label-").concat(d),
                    text: u,
                    datum: s,
                    activePoints: f,
                    textAnchor: y,
                    dy: i,
                    dx: l,
                    style: r,
                    x:
                      (function () {
                        if (!y || "middle" === y) return n.x;
                        var t = "end" === y ? -1 : 1;
                        return n.x - t * (o.width / 2);
                      })() +
                      (v.left - v.right) / 2,
                    y: n.y + (v.top - v.bottom) / 2,
                    verticalAnchor: "middle",
                    angle: r.angle,
                  });
                },
              },
              {
                key: "getPointerOrientation",
                value: function (t, e, n) {
                  var r = e.y + n.height / 2,
                    o = e.y - n.height / 2,
                    a = e.x - n.width / 2,
                    i = e.x + n.width / 2,
                    c = [
                      { side: "top", val: o > t.y ? o - t.y : -1 },
                      { side: "bottom", val: r < t.y ? t.y - r : -1 },
                      { side: "right", val: i < t.x ? t.x - i : -1 },
                      { side: "left", val: a > t.x ? a - t.x : -1 },
                    ];
                  return l()(c, "val", "desc")[0].side;
                },
              },
              {
                key: "getFlyoutProps",
                value: function (t, e) {
                  var n = e.flyoutDimensions,
                    r = e.flyoutStyle,
                    o = e.flyoutCenter,
                    a = t.x,
                    i = t.y,
                    c = t.dx,
                    l = t.dy,
                    u = t.datum,
                    s = t.activePoints,
                    f = t.index,
                    p = t.pointerLength,
                    d = t.pointerWidth,
                    v = t.cornerRadius,
                    y = t.events,
                    m = t.flyoutComponent,
                    g = O.xs(t.pointerOrientation, t);
                  return h()({}, m.props, {
                    x: a,
                    y: i,
                    dx: c,
                    dy: l,
                    datum: u,
                    activePoints: s,
                    index: f,
                    pointerLength: p,
                    pointerWidth: d,
                    cornerRadius: v,
                    events: y,
                    orientation:
                      g || this.getPointerOrientation({ x: a, y: i }, o, n),
                    key: "".concat(this.id, "-tooltip-").concat(f),
                    width: n.width,
                    height: n.height,
                    style: r,
                    center: o,
                  });
                },
              },
              {
                key: "renderTooltip",
                value: function (t) {
                  var e = O.xs(t.active, t),
                    n = t.renderInPortal;
                  if (!e) return n ? o.createElement(C.V, null, null) : null;
                  var r = this.getEvaluatedProps(t),
                    a = r.flyoutComponent,
                    i = r.labelComponent,
                    c = r.groupComponent,
                    l = this.getCalculatedValues(r),
                    u = [
                      o.cloneElement(a, this.getFlyoutProps(r, l)),
                      o.cloneElement(i, this.getLabelProps(r, l)),
                    ],
                    s = o.cloneElement(
                      c,
                      { role: "presentation", transform: l.transform },
                      u,
                    );
                  return n ? o.createElement(C.V, null, s) : s;
                },
              },
              {
                key: "render",
                value: function () {
                  var t = O.TY(this.props, U, "tooltip");
                  return this.renderTooltip(t);
                },
              },
            ]) && N(e.prototype, n),
            r && N(e, r),
            Object.defineProperty(e, "prototype", { writable: !1 }),
            i
          );
        })(o.Component);
      (B.displayName = "VictoryTooltip"),
        (B.role = "tooltip"),
        (B.propTypes = {
          activateData: g().bool,
          active: g().oneOfType([g().bool, g().func]),
          activePoints: g().array,
          angle: g().number,
          center: g().shape({ x: S.A7, y: S.A7 }),
          centerOffset: g().shape({
            x: g().oneOfType([g().number, g().func]),
            y: g().oneOfType([g().number, g().func]),
          }),
          constrainToVisibleArea: g().bool,
          cornerRadius: g().oneOfType([S.A7, g().func]),
          data: g().array,
          datum: g().object,
          dx: g().oneOfType([g().number, g().func]),
          dy: g().oneOfType([g().number, g().func]),
          events: g().object,
          flyoutComponent: g().element,
          flyoutHeight: g().oneOfType([S.A7, g().func]),
          flyoutPadding: g().oneOfType([
            g().func,
            g().number,
            g().shape({
              top: g().number,
              bottom: g().number,
              left: g().number,
              right: g().number,
            }),
          ]),
          flyoutStyle: g().object,
          flyoutWidth: g().oneOfType([S.A7, g().func]),
          groupComponent: g().element,
          height: g().number,
          horizontal: g().bool,
          id: g().oneOfType([g().number, g().string]),
          index: g().oneOfType([g().number, g().string]),
          labelComponent: g().element,
          orientation: g().oneOfType([
            g().oneOf(["top", "bottom", "left", "right"]),
            g().func,
          ]),
          pointerLength: g().oneOfType([S.A7, g().func]),
          pointerOrientation: g().oneOfType([
            g().oneOf(["top", "bottom", "left", "right"]),
            g().func,
          ]),
          pointerWidth: g().oneOfType([S.A7, g().func]),
          polar: g().bool,
          renderInPortal: g().bool,
          scale: g().shape({ x: S.bA, y: S.bA }),
          style: g().oneOfType([g().object, g().array]),
          text: g().oneOfType([g().string, g().number, g().func, g().array]),
          theme: g().object,
          width: g().number,
          x: g().number,
          y: g().number,
        }),
        (B.defaultProps = {
          active: !1,
          renderInPortal: !0,
          labelComponent: o.createElement(A.X, null),
          flyoutComponent: o.createElement(D, null),
          groupComponent: o.createElement("g", null),
        }),
        (B.defaultEvents = function (t) {
          var e = t.activateData
              ? [
                  {
                    target: "labels",
                    mutation: function () {
                      return { active: !0 };
                    },
                  },
                  {
                    target: "data",
                    mutation: function () {
                      return { active: !0 };
                    },
                  },
                ]
              : [
                  {
                    target: "labels",
                    mutation: function () {
                      return { active: !0 };
                    },
                  },
                ],
            n = t.activateData
              ? [
                  {
                    target: "labels",
                    mutation: function () {
                      return { active: void 0 };
                    },
                  },
                  {
                    target: "data",
                    mutation: function () {
                      return { active: void 0 };
                    },
                  },
                ]
              : [
                  {
                    target: "labels",
                    mutation: function () {
                      return { active: void 0 };
                    },
                  },
                ];
          return [
            {
              target: "data",
              eventHandlers: {
                onMouseOver: function () {
                  return e;
                },
                onFocus: function () {
                  return e;
                },
                onTouchStart: function () {
                  return e;
                },
                onMouseOut: function () {
                  return n;
                },
                onBlur: function () {
                  return n;
                },
                onTouchEnd: function () {
                  return n;
                },
              },
            },
          ];
        });
      var q = n(77534),
        H = n(79674);
      const V = (t) => {
        var {
            constrainToVisibleArea: e = !1,
            labelComponent: n = o.createElement(q.D, null),
            labelTextAnchor: a,
            themeColor: i,
            theme: c = (0, H.gh)(i),
          } = t,
          l = (0, r.__rest)(t, [
            "constrainToVisibleArea",
            "labelComponent",
            "labelTextAnchor",
            "themeColor",
            "theme",
          ]);
        const u = o.cloneElement(
          n,
          Object.assign({ textAnchor: a, theme: c }, n.props),
        );
        return o.createElement(
          B,
          Object.assign(
            { constrainToVisibleArea: e, labelComponent: u, theme: c },
            l,
          ),
        );
      };
      (V.displayName = "ChartTooltip"), i()(V, B);
    },
    70219: (t, e, n) => {
      "use strict";
      n.d(e, { g: () => r });
      "undefined" === typeof window ||
        !window.document ||
        window.document.createElement;
      const r = (t) => {
        let e,
          { className: n } = t;
        return (
          n &&
            (e = n
              .replace(/VictoryContainer/g, "")
              .replace(/pf-v5-c-chart/g, "")
              .replace(/pf-c-chart/g, "")
              .replace(/\s+/g, " ")
              .trim()),
          e && e.length ? "pf-v5-c-chart ".concat(e) : "pf-v5-c-chart"
        );
      };
    },
    10859: (t, e, n) => {
      "use strict";
      n.d(e, { LF: () => u, cA: () => p, im: () => d, xA: () => f });
      var r = n(75971),
        o = n(72791),
        a = n(30804),
        i = n.n(a);
      const c = [
          {
            d: "M 0 0 L 5 5 M 4.5 -0.5 L 5.5 0.5 M -0.5 4.5 L 0.5 5.5",
            height: 5,
            fill: "none",
            patternContentUnits: "userSpaceOnUse",
            patternUnits: "userSpaceOnUse",
            patternTransform: "scale(1.4 1.4)",
            strokeWidth: 2,
            width: 5,
            x: 0,
            y: 0,
          },
          {
            d: "M 0 5 L 5 0 M -0.5 0.5 L 0.5 -0.5 M 4.5 5.5 L 5.5 4.5",
            height: 5,
            fill: "none",
            patternContentUnits: "userSpaceOnUse",
            patternUnits: "userSpaceOnUse",
            patternTransform: "scale(1.4 1.4)",
            strokeWidth: 2,
            width: 5,
            x: 0,
            y: 0,
          },
          {
            d: "M 2 0 L 2 5 M 4 0 L 4 5",
            height: 5,
            fill: "none",
            patternContentUnits: "userSpaceOnUse",
            patternUnits: "userSpaceOnUse",
            patternTransform: "scale(1.4 1.4)",
            strokeWidth: 2,
            width: 5,
            x: 0,
            y: 0,
          },
          {
            d: "M 0 2 L 5 2 M 0 4 L 5 4",
            height: 5,
            fill: "none",
            patternContentUnits: "userSpaceOnUse",
            patternUnits: "userSpaceOnUse",
            patternTransform: "scale(1.4 1.4)",
            strokeWidth: 2,
            width: 5,
            x: 0,
            y: 0,
          },
          {
            d: "M 0 1.5 L 2.5 1.5 L 2.5 0 M 2.5 5 L 2.5 3.5 L 5 3.5",
            height: 5,
            fill: "none",
            patternContentUnits: "userSpaceOnUse",
            patternUnits: "userSpaceOnUse",
            patternTransform: "scale(1.4 1.4)",
            strokeWidth: 2,
            width: 5,
            x: 0,
            y: 0,
          },
          {
            d: "M 0 0 L 5 10 L 10 0",
            height: 10,
            fill: "none",
            patternContentUnits: "userSpaceOnUse",
            patternUnits: "userSpaceOnUse",
            strokeWidth: 2,
            width: 10,
            x: 0,
            y: 0,
          },
          {
            d: "M 3 3 L 8 3 L 8 8 L 3 8 Z",
            height: 10,
            fill: "none",
            patternContentUnits: "userSpaceOnUse",
            patternUnits: "userSpaceOnUse",
            strokeWidth: 2,
            width: 10,
            x: 0,
            y: 0,
          },
          {
            d: "M 5 5 m -4 0 a 4 4 0 1 1 8 0 a 4 4 0 1 1 -8 0",
            height: 10,
            fill: "none",
            patternContentUnits: "userSpaceOnUse",
            patternUnits: "userSpaceOnUse",
            strokeWidth: 2,
            width: 10,
            x: 0,
            y: 0,
          },
          {
            d: "M 0 0 L 10 10 M 9 -1 L 11 1 M -1 9 L 1 11",
            height: 10,
            fill: "none",
            patternContentUnits: "userSpaceOnUse",
            patternUnits: "userSpaceOnUse",
            strokeWidth: 2,
            width: 10,
            x: 0,
            y: 0,
          },
          {
            d: "M 0 10 L 10 0 M -1 1 L 1 -1 M 9 11 L 11 9",
            height: 10,
            fill: "none",
            patternContentUnits: "userSpaceOnUse",
            patternUnits: "userSpaceOnUse",
            strokeWidth: 2,
            width: 10,
            x: 0,
            y: 0,
          },
          {
            d: "M 2 5 L 5 2 L 8 5 L 5 8 Z",
            height: 10,
            fill: "none",
            patternContentUnits: "userSpaceOnUse",
            patternUnits: "userSpaceOnUse",
            strokeWidth: 2,
            width: 10,
            x: 0,
            y: 0,
          },
          {
            d: "M 3 0 L 3 10 M 8 0 L 8 10",
            height: 5,
            fill: "none",
            patternContentUnits: "userSpaceOnUse",
            patternUnits: "userSpaceOnUse",
            patternTransform: "scale(1.4 1.4)",
            strokeWidth: 2,
            width: 5,
            x: 0,
            y: 0,
          },
          {
            d: "M 10 3 L 5 3 L 5 0 M 5 10 L 5 7 L 0 7",
            height: 10,
            fill: "none",
            patternContentUnits: "userSpaceOnUse",
            patternUnits: "userSpaceOnUse",
            strokeWidth: 2,
            width: 10,
            x: 0,
            y: 0,
          },
          {
            d: "M 0 3 L 10 3 M 0 8 L 10 8",
            height: 5,
            fill: "none",
            patternContentUnits: "userSpaceOnUse",
            patternUnits: "userSpaceOnUse",
            patternTransform: "scale(1.4 1.4)",
            strokeWidth: 2,
            width: 5,
            x: 0,
            y: 0,
          },
          {
            d: "M 0 3 L 5 3 L 5 0 M 5 10 L 5 7 L 10 7",
            height: 10,
            fill: "none",
            patternContentUnits: "userSpaceOnUse",
            patternUnits: "userSpaceOnUse",
            strokeWidth: 2,
            width: 10,
            x: 0,
            y: 0,
          },
        ],
        l = (t, e) => "".concat(t, ":").concat(e),
        u = (t) => {
          let {
            colorScale: e,
            offset: n = 0,
            patternId: a,
            patternUnshiftIndex: i = 0,
          } = t;
          const u = [...c];
          i > 0 && i < u.length && u.unshift(u.splice(i, 1)[0]);
          return o.createElement(
            o.Fragment,
            { key: "defs" },
            o.createElement(
              "defs",
              null,
              e.map((t, e) => {
                const i = u[(e + n) % u.length],
                  { d: c, fill: s, stroke: f = t, strokeWidth: p } = i,
                  d = (0, r.__rest)(i, ["d", "fill", "stroke", "strokeWidth"]),
                  h = l(a, e);
                return o.createElement(
                  "pattern",
                  Object.assign({ id: h, key: h }, d),
                  o.createElement("path", {
                    d: c,
                    stroke: f,
                    strokeWidth: p,
                    fill: s,
                  }),
                );
              }),
            ),
          );
        },
        s = (t) => {
          let { colorScale: e, patternId: n, patternScale: r } = t;
          if (r) return r;
          const o = ((t, e) => t.map((t, n) => "url(#".concat(l(e, n), ")")))(
            e,
            n,
          );
          return o && o.length > 0 ? o : void 0;
        },
        f = (t, e) =>
          e
            ? t.map((t, n) => {
                const r = e[n % e.length];
                return Object.assign(Object.assign({}, r && { _fill: r }), t);
              })
            : t,
        p = (t) => {
          let {
            colorScale: e,
            hasPatterns: n,
            patternScale: r,
            themeColorScale: a,
          } = t;
          const c = ((t, e) => {
            const n = [];
            return (t || e).forEach((t) => n.push(t)), n;
          })(e, a);
          let l = r,
            u = !r && void 0 !== n;
          const f = o.useMemo(() => (u ? i()("pf-pattern") : void 0), [u]);
          if (
            (u && (l = s({ colorScale: c, patternId: f, patternScale: r })),
            Array.isArray(n))
          )
            for (let o = 0; o < l.length; o++)
              (o < n.length && n[o]) || (l[o] = null);
          else !1 === n && ((l = void 0), (u = !1));
          return {
            defaultColorScale: c,
            defaultPatternScale: l,
            isPatternDefs: u,
            patternId: f,
          };
        },
        d = (t) => {
          let { children: e, patternScale: n } = t;
          return o.Children.toArray(e).map((t, e) => {
            if (o.isValidElement(t)) {
              const a = (0, r.__rest)(t.props, []),
                i = a.style ? Object.assign({}, a.style) : {};
              if (n) {
                const t = n[e % n.length];
                i.data = Object.assign(
                  Object.assign({}, t && { fill: t }),
                  i.data,
                );
              }
              return o.cloneElement(
                t,
                Object.assign(
                  Object.assign(Object.assign({}, n && { patternScale: n }), a),
                  { style: i },
                ),
              );
            }
            return t;
          });
        };
    },
    7953: (t, e, n) => {
      "use strict";
      n.d(e, { EH: () => i, zU: () => a });
      n(58121);
      var r = n(40005),
        o = n(79674);
      const a = (t) => (0, o.jp)(t, r.fm),
        i = (t, e) => {
          const n = (0, o.gh)(t);
          return (
            e ||
              ((n.axis.padding = 0),
              (n.axis.style.axis.fill = "none"),
              (n.axis.style.axis.stroke = "none"),
              (n.axis.style.grid.fill = "none"),
              (n.axis.style.grid.stroke = "none"),
              (n.axis.style.ticks.fill = "none"),
              (n.axis.style.ticks.stroke = "none"),
              (n.axis.style.tickLabels.fill = "none")),
            n
          );
        };
    },
    79674: (t, e, n) => {
      "use strict";
      n.d(e, { jp: () => C, gh: () => S });
      var r = n(79286),
        o = n.n(r),
        a = n(87296),
        i = n(40005);
      const c = {
          name: "--pf-v5-chart-theme--blue--ColorScale--100",
          value: "#06c",
          var: "var(--pf-v5-chart-theme--blue--ColorScale--100, #06c)",
        },
        l = {
          name: "--pf-v5-chart-theme--blue--ColorScale--200",
          value: "#8bc1f7",
          var: "var(--pf-v5-chart-theme--blue--ColorScale--200, #8bc1f7)",
        },
        u = {
          name: "--pf-v5-chart-theme--blue--ColorScale--300",
          value: "#002f5d",
          var: "var(--pf-v5-chart-theme--blue--ColorScale--300, #002f5d)",
        },
        s = {
          name: "--pf-v5-chart-theme--blue--ColorScale--400",
          value: "#519de9",
          var: "var(--pf-v5-chart-theme--blue--ColorScale--400, #519de9)",
        },
        f = {
          name: "--pf-v5-chart-theme--blue--ColorScale--500",
          value: "#004b95",
          var: "var(--pf-v5-chart-theme--blue--ColorScale--500, #004b95)",
        },
        p = (t) => {
          const { COLOR_SCALE: e } = t;
          return {
            area: { colorScale: e, style: { data: { fill: e[0] } } },
            axis: { colorScale: e },
            bar: { colorScale: e, style: { data: { fill: e[0] } } },
            boxplot: {
              colorScale: e,
              style: { q1: { fill: e[0] }, q3: { fill: e[0] } },
            },
            candlestick: { colorScale: e },
            chart: { colorScale: e },
            errorbar: { colorScale: e },
            group: { colorScale: e },
            legend: { colorScale: e },
            line: { colorScale: e, style: { data: { stroke: e[0] } } },
            pie: { colorScale: e },
            scatter: { colorScale: e },
            stack: { colorScale: e },
            voronoi: { colorScale: e },
          };
        },
        d = [c.var, l.var, u.var, s.var, f.var],
        h = p({ COLOR_SCALE: d }),
        v = p({
          COLOR_SCALE: [
            {
              name: "--pf-v5-chart-theme--cyan--ColorScale--100",
              value: "#009596",
              var: "var(--pf-v5-chart-theme--cyan--ColorScale--100, #009596)",
            }.var,
            {
              name: "--pf-v5-chart-theme--cyan--ColorScale--200",
              value: "#a2d9d9",
              var: "var(--pf-v5-chart-theme--cyan--ColorScale--200, #a2d9d9)",
            }.var,
            {
              name: "--pf-v5-chart-theme--cyan--ColorScale--300",
              value: "#003737",
              var: "var(--pf-v5-chart-theme--cyan--ColorScale--300, #003737)",
            }.var,
            {
              name: "--pf-v5-chart-theme--cyan--ColorScale--400",
              value: "#73c5c5",
              var: "var(--pf-v5-chart-theme--cyan--ColorScale--400, #73c5c5)",
            }.var,
            {
              name: "--pf-v5-chart-theme--cyan--ColorScale--500",
              value: "#005f60",
              var: "var(--pf-v5-chart-theme--cyan--ColorScale--500, #005f60)",
            }.var,
          ],
        }),
        y = p({
          COLOR_SCALE: [
            {
              name: "--pf-v5-chart-theme--gold--ColorScale--100",
              value: "#f4c145",
              var: "var(--pf-v5-chart-theme--gold--ColorScale--100, #f4c145)",
            }.var,
            {
              name: "--pf-v5-chart-theme--gold--ColorScale--200",
              value: "#f9e0a2",
              var: "var(--pf-v5-chart-theme--gold--ColorScale--200, #f9e0a2)",
            }.var,
            {
              name: "--pf-v5-chart-theme--gold--ColorScale--300",
              value: "#c58c00",
              var: "var(--pf-v5-chart-theme--gold--ColorScale--300, #c58c00)",
            }.var,
            {
              name: "--pf-v5-chart-theme--gold--ColorScale--400",
              value: "#f6d173",
              var: "var(--pf-v5-chart-theme--gold--ColorScale--400, #f6d173)",
            }.var,
            {
              name: "--pf-v5-chart-theme--gold--ColorScale--500",
              value: "#f0ab00",
              var: "var(--pf-v5-chart-theme--gold--ColorScale--500, #f0ab00)",
            }.var,
          ],
        }),
        m = p({
          COLOR_SCALE: [
            {
              name: "--pf-v5-chart-theme--gray--ColorScale--100",
              value: "#b8bbbe",
              var: "var(--pf-v5-chart-theme--gray--ColorScale--100, #b8bbbe)",
            }.var,
            {
              name: "--pf-v5-chart-theme--gray--ColorScale--200",
              value: "#f0f0f0",
              var: "var(--pf-v5-chart-theme--gray--ColorScale--200, #f0f0f0)",
            }.var,
            {
              name: "--pf-v5-chart-theme--gray--ColorScale--300",
              value: "#6a6e73",
              var: "var(--pf-v5-chart-theme--gray--ColorScale--300, #6a6e73)",
            }.var,
            {
              name: "--pf-v5-chart-theme--gray--ColorScale--400",
              value: "#d2d2d2",
              var: "var(--pf-v5-chart-theme--gray--ColorScale--400, #d2d2d2)",
            }.var,
            {
              name: "--pf-v5-chart-theme--gray--ColorScale--500",
              value: "#8a8d90",
              var: "var(--pf-v5-chart-theme--gray--ColorScale--500, #8a8d90)",
            }.var,
          ],
        }),
        g = p({
          COLOR_SCALE: [
            {
              name: "--pf-v5-chart-theme--green--ColorScale--100",
              value: "#4cb140",
              var: "var(--pf-v5-chart-theme--green--ColorScale--100, #4cb140)",
            }.var,
            {
              name: "--pf-v5-chart-theme--green--ColorScale--200",
              value: "#bde2b9",
              var: "var(--pf-v5-chart-theme--green--ColorScale--200, #bde2b9)",
            }.var,
            {
              name: "--pf-v5-chart-theme--green--ColorScale--300",
              value: "#23511e",
              var: "var(--pf-v5-chart-theme--green--ColorScale--300, #23511e)",
            }.var,
            {
              name: "--pf-v5-chart-theme--green--ColorScale--400",
              value: "#7cc674",
              var: "var(--pf-v5-chart-theme--green--ColorScale--400, #7cc674)",
            }.var,
            {
              name: "--pf-v5-chart-theme--green--ColorScale--500",
              value: "#38812f",
              var: "var(--pf-v5-chart-theme--green--ColorScale--500, #38812f)",
            }.var,
          ],
        }),
        b = p({
          COLOR_SCALE: [
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--100",
              value: "#06c",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--100, #06c)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--200",
              value: "#4cb140",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--200, #4cb140)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--300",
              value: "#009596",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--300, #009596)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--400",
              value: "#f4c145",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--400, #f4c145)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--500",
              value: "#ec7a08",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--500, #ec7a08)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--600",
              value: "#8bc1f7",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--600, #8bc1f7)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--700",
              value: "#23511e",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--700, #23511e)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--800",
              value: "#a2d9d9",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--800, #a2d9d9)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--900",
              value: "#f9e0a2",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--900, #f9e0a2)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--1000",
              value: "#8f4700",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--1000, #8f4700)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--1100",
              value: "#002f5d",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--1100, #002f5d)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--1200",
              value: "#bde2b9",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--1200, #bde2b9)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--1300",
              value: "#003737",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--1300, #003737)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--1400",
              value: "#c58c00",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--1400, #c58c00)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--1500",
              value: "#f4b678",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--1500, #f4b678)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--1600",
              value: "#519de9",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--1600, #519de9)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--1700",
              value: "#38812f",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--1700, #38812f)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--1800",
              value: "#73c5c5",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--1800, #73c5c5)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--1900",
              value: "#f6d173",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--1900, #f6d173)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--2000",
              value: "#c46100",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--2000, #c46100)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--2100",
              value: "#004b95",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--2100, #004b95)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--2200",
              value: "#7cc674",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--2200, #7cc674)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--2300",
              value: "#005f60",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--2300, #005f60)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--2400",
              value: "#f0ab00",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--2400, #f0ab00)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-ordered--ColorScale--2500",
              value: "#ef9234",
              var: "var(--pf-v5-chart-theme--multi-color-ordered--ColorScale--2500, #ef9234)",
            }.var,
          ],
        }),
        x = p({
          COLOR_SCALE: [
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--100",
              value: "#06c",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--100, #06c)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--200",
              value: "#f4c145",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--200, #f4c145)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--300",
              value: "#4cb140",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--300, #4cb140)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--400",
              value: "#5752d1",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--400, #5752d1)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--500",
              value: "#ec7a08",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--500, #ec7a08)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--600",
              value: "#009596",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--600, #009596)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--700",
              value: "#b8bbbe",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--700, #b8bbbe)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--800",
              value: "#8bc1f7",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--800, #8bc1f7)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--900",
              value: "#c58c00",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--900, #c58c00)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--1000",
              value: "#bde2b9",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--1000, #bde2b9)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--1100",
              value: "#2a265f",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--1100, #2a265f)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--1200",
              value: "#f4b678",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--1200, #f4b678)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--1300",
              value: "#003737",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--1300, #003737)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--1400",
              value: "#f0f0f0",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--1400, #f0f0f0)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--1500",
              value: "#002f5d",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--1500, #002f5d)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--1600",
              value: "#f9e0a2",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--1600, #f9e0a2)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--1700",
              value: "#23511e",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--1700, #23511e)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--1800",
              value: "#b2b0ea",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--1800, #b2b0ea)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--1900",
              value: "#8f4700",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--1900, #8f4700)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--2000",
              value: "#a2d9d9",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--2000, #a2d9d9)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--2100",
              value: "#6a6e73",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--2100, #6a6e73)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--2200",
              value: "#519de9",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--2200, #519de9)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--2300",
              value: "#f0ab00",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--2300, #f0ab00)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--2400",
              value: "#7cc674",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--2400, #7cc674)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--2500",
              value: "#3c3d99",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--2500, #3c3d99)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--2600",
              value: "#ef9234",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--2600, #ef9234)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--2700",
              value: "#005f60",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--2700, #005f60)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--2800",
              value: "#d2d2d2",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--2800, #d2d2d2)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--2900",
              value: "#004b95",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--2900, #004b95)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--3000",
              value: "#f6d173",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--3000, #f6d173)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--3100",
              value: "#38812f",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--3100, #38812f)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--3200",
              value: "#8481dd",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--3200, #8481dd)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--3300",
              value: "#c46100",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--3300, #c46100)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--3400",
              value: "#73c5c5",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--3400, #73c5c5)",
            }.var,
            {
              name: "--pf-v5-chart-theme--multi-color-unordered--ColorScale--3500",
              value: "#8a8d90",
              var: "var(--pf-v5-chart-theme--multi-color-unordered--ColorScale--3500, #8a8d90)",
            }.var,
          ],
        }),
        O = p({
          COLOR_SCALE: [
            {
              name: "--pf-v5-chart-theme--orange--ColorScale--100",
              value: "#ec7a08",
              var: "var(--pf-v5-chart-theme--orange--ColorScale--100, #ec7a08)",
            }.var,
            {
              name: "--pf-v5-chart-theme--orange--ColorScale--200",
              value: "#f4b678",
              var: "var(--pf-v5-chart-theme--orange--ColorScale--200, #f4b678)",
            }.var,
            {
              name: "--pf-v5-chart-theme--orange--ColorScale--300",
              value: "#8f4700",
              var: "var(--pf-v5-chart-theme--orange--ColorScale--300, #8f4700)",
            }.var,
            {
              name: "--pf-v5-chart-theme--orange--ColorScale--400",
              value: "#ef9234",
              var: "var(--pf-v5-chart-theme--orange--ColorScale--400, #ef9234)",
            }.var,
            {
              name: "--pf-v5-chart-theme--orange--ColorScale--500",
              value: "#c46100",
              var: "var(--pf-v5-chart-theme--orange--ColorScale--500, #c46100)",
            }.var,
          ],
        }),
        w = p({
          COLOR_SCALE: [
            {
              name: "--pf-v5-chart-theme--purple--ColorScale--100",
              value: "#5752d1",
              var: "var(--pf-v5-chart-theme--purple--ColorScale--100, #5752d1)",
            }.var,
            {
              name: "--pf-v5-chart-theme--purple--ColorScale--200",
              value: "#b2b0ea",
              var: "var(--pf-v5-chart-theme--purple--ColorScale--200, #b2b0ea)",
            }.var,
            {
              name: "--pf-v5-chart-theme--purple--ColorScale--300",
              value: "#2a265f",
              var: "var(--pf-v5-chart-theme--purple--ColorScale--300, #2a265f)",
            }.var,
            {
              name: "--pf-v5-chart-theme--purple--ColorScale--400",
              value: "#8481dd",
              var: "var(--pf-v5-chart-theme--purple--ColorScale--400, #8481dd)",
            }.var,
            {
              name: "--pf-v5-chart-theme--purple--ColorScale--500",
              value: "#3c3d99",
              var: "var(--pf-v5-chart-theme--purple--ColorScale--500, #3c3d99)",
            }.var,
          ],
        }),
        C = (t, e) => o()(S(t), e),
        S = (t) => {
          const e = Object.assign({}, JSON.parse(JSON.stringify(i.kJ)));
          return o()(e, A(t));
        },
        A = (t) => {
          switch (t) {
            case a.n.blue:
              return h;
            case a.n.cyan:
              return v;
            case a.n.gold:
              return y;
            case a.n.gray:
              return m;
            case a.n.green:
              return g;
            case a.n.multi:
            case a.n.multiOrdered:
              return b;
            case a.n.multiUnordered:
              return x;
            case a.n.orange:
              return O;
            case a.n.purple:
              return w;
            default:
              return h;
          }
        };
    },
    35684: (t, e, n) => {
      "use strict";
      n.d(e, { Z: () => r });
      const r = {
        name: "--pf-v5-chart-global--FontFamily",
        value: '"RedHatText", helvetica, arial, sans-serif',
        var: 'var(--pf-v5-chart-global--FontFamily, "RedHatText", helvetica, arial, sans-serif)',
      };
    },
    67690: (t, e, n) => {
      "use strict";
      n.d(e, { Z: () => r });
      const r = {
        name: "--pf-v5-chart-global--FontSize--sm",
        value: 14,
        var: "var(--pf-v5-chart-global--FontSize--sm, 14)",
      };
    },
    85134: (t, e, n) => {
      "use strict";
      n.d(e, { Z: () => r });
      const r = {
        name: "--pf-v5-chart-global--label--Fill",
        value: "#151515",
        var: "var(--pf-v5-chart-global--label--Fill, #151515)",
      };
    },
    18769: (t, e, n) => {
      "use strict";
      n.d(e, { Z: () => r });
      const r = {
        name: "--pf-v5-chart-global--letter-spacing",
        value: "normal",
        var: "var(--pf-v5-chart-global--letter-spacing, normal)",
      };
    },
    18425: (t, e, n) => {
      "use strict";
      n.d(e, { Z: () => r });
      const r = {
        name: "--pf-v5-chart-legend--Margin",
        value: 16,
        var: "var(--pf-v5-chart-legend--Margin, 16)",
      };
    },
    62110: (t, e, n) => {
      "use strict";
      var r = n(57441),
        o = {
          childContextTypes: !0,
          contextType: !0,
          contextTypes: !0,
          defaultProps: !0,
          displayName: !0,
          getDefaultProps: !0,
          getDerivedStateFromError: !0,
          getDerivedStateFromProps: !0,
          mixins: !0,
          propTypes: !0,
          type: !0,
        },
        a = {
          name: !0,
          length: !0,
          prototype: !0,
          caller: !0,
          callee: !0,
          arguments: !0,
          arity: !0,
        },
        i = {
          $$typeof: !0,
          compare: !0,
          defaultProps: !0,
          displayName: !0,
          propTypes: !0,
          type: !0,
        },
        c = {};
      function l(t) {
        return r.isMemo(t) ? i : c[t.$$typeof] || o;
      }
      (c[r.ForwardRef] = {
        $$typeof: !0,
        render: !0,
        defaultProps: !0,
        displayName: !0,
        propTypes: !0,
      }),
        (c[r.Memo] = i);
      var u = Object.defineProperty,
        s = Object.getOwnPropertyNames,
        f = Object.getOwnPropertySymbols,
        p = Object.getOwnPropertyDescriptor,
        d = Object.getPrototypeOf,
        h = Object.prototype;
      t.exports = function t(e, n, r) {
        if ("string" !== typeof n) {
          if (h) {
            var o = d(n);
            o && o !== h && t(e, o, r);
          }
          var i = s(n);
          f && (i = i.concat(f(n)));
          for (var c = l(e), v = l(n), y = 0; y < i.length; ++y) {
            var m = i[y];
            if (!a[m] && (!r || !r[m]) && (!v || !v[m]) && (!c || !c[m])) {
              var g = p(n, m);
              try {
                u(e, m, g);
              } catch (b) {}
            }
          }
        }
        return e;
      };
    },
    72451: (t, e) => {
      function n(t, e) {
        var n = [],
          r = [];
        return (
          null == e &&
            (e = function (t, e) {
              return n[0] === e
                ? "[Circular ~]"
                : "[Circular ~." + r.slice(0, n.indexOf(e)).join(".") + "]";
            }),
          function (o, a) {
            if (n.length > 0) {
              var i = n.indexOf(this);
              ~i ? n.splice(i + 1) : n.push(this),
                ~i ? r.splice(i, 1 / 0, o) : r.push(o),
                ~n.indexOf(a) && (a = e.call(this, o, a));
            } else n.push(a);
            return null == t ? a : t.call(this, o, a);
          }
        );
      }
      (t.exports = function (t, e, r, o) {
        return JSON.stringify(t, n(e, o), r);
      }).getSerialize = n;
    },
    50908: (t, e, n) => {
      var r = n(68136)(n(97009), "DataView");
      t.exports = r;
    },
    78319: (t, e, n) => {
      var r = n(68136)(n(97009), "Promise");
      t.exports = r;
    },
    23924: (t, e, n) => {
      var r = n(68136)(n(97009), "Set");
      t.exports = r;
    },
    20692: (t, e, n) => {
      var r = n(78059),
        o = n(35774),
        a = n(41596);
      function i(t) {
        var e = -1,
          n = null == t ? 0 : t.length;
        for (this.__data__ = new r(); ++e < n; ) this.add(t[e]);
      }
      (i.prototype.add = i.prototype.push = o),
        (i.prototype.has = a),
        (t.exports = i);
    },
    7091: (t, e, n) => {
      var r = n(68136)(n(97009), "WeakMap");
      t.exports = r;
    },
    31211: (t) => {
      t.exports = function (t, e, n, r) {
        for (var o = -1, a = null == t ? 0 : t.length; ++o < a; ) {
          var i = t[o];
          e(r, i, n(i), t);
        }
        return r;
      };
    },
    4550: (t) => {
      t.exports = function (t, e) {
        for (
          var n = -1, r = null == t ? 0 : t.length;
          ++n < r && !1 !== e(t[n], n, t);

        );
        return t;
      };
    },
    84903: (t) => {
      t.exports = function (t, e) {
        for (
          var n = -1, r = null == t ? 0 : t.length, o = 0, a = [];
          ++n < r;

        ) {
          var i = t[n];
          e(i, n, t) && (a[o++] = i);
        }
        return a;
      };
    },
    59055: (t, e, n) => {
      var r = n(24842);
      t.exports = function (t, e) {
        return !!(null == t ? 0 : t.length) && r(t, e, 0) > -1;
      };
    },
    32683: (t) => {
      t.exports = function (t, e, n) {
        for (var r = -1, o = null == t ? 0 : t.length; ++r < o; )
          if (n(e, t[r])) return !0;
        return !1;
      };
    },
    68950: (t) => {
      t.exports = function (t, e) {
        for (var n = -1, r = null == t ? 0 : t.length, o = Array(r); ++n < r; )
          o[n] = e(t[n], n, t);
        return o;
      };
    },
    41705: (t) => {
      t.exports = function (t, e) {
        for (var n = -1, r = e.length, o = t.length; ++n < r; ) t[o + n] = e[n];
        return t;
      };
    },
    47897: (t) => {
      t.exports = function (t, e) {
        for (var n = -1, r = null == t ? 0 : t.length; ++n < r; )
          if (e(t[n], n, t)) return !0;
        return !1;
      };
    },
    38430: (t, e, n) => {
      var r = n(87927);
      t.exports = function (t, e, n, o) {
        return (
          r(t, function (t, r, a) {
            e(o, t, n(t), a);
          }),
          o
        );
      };
    },
    11855: (t, e, n) => {
      var r = n(64503),
        o = n(12742);
      t.exports = function (t, e) {
        return t && r(e, o(e), t);
      };
    },
    95076: (t, e, n) => {
      var r = n(64503),
        o = n(73961);
      t.exports = function (t, e) {
        return t && r(e, o(e), t);
      };
    },
    31905: (t, e, n) => {
      var r = n(22854),
        o = n(4550),
        a = n(18463),
        i = n(11855),
        c = n(95076),
        l = n(94523),
        u = n(10291),
        s = n(52455),
        f = n(57636),
        p = n(38248),
        d = n(55341),
        h = n(88383),
        v = n(39243),
        y = n(39759),
        m = n(40548),
        g = n(93629),
        b = n(5174),
        x = n(60103),
        O = n(8092),
        w = n(36995),
        C = n(12742),
        S = n(73961),
        A = "[object Arguments]",
        j = "[object Function]",
        k = "[object Object]",
        P = {};
      (P[A] =
        P["[object Array]"] =
        P["[object ArrayBuffer]"] =
        P["[object DataView]"] =
        P["[object Boolean]"] =
        P["[object Date]"] =
        P["[object Float32Array]"] =
        P["[object Float64Array]"] =
        P["[object Int8Array]"] =
        P["[object Int16Array]"] =
        P["[object Int32Array]"] =
        P["[object Map]"] =
        P["[object Number]"] =
        P[k] =
        P["[object RegExp]"] =
        P["[object Set]"] =
        P["[object String]"] =
        P["[object Symbol]"] =
        P["[object Uint8Array]"] =
        P["[object Uint8ClampedArray]"] =
        P["[object Uint16Array]"] =
        P["[object Uint32Array]"] =
          !0),
        (P["[object Error]"] = P[j] = P["[object WeakMap]"] = !1),
        (t.exports = function t(e, n, E, M, T, _) {
          var L,
            D = 1 & n,
            I = 2 & n,
            R = 4 & n;
          if ((E && (L = T ? E(e, M, T, _) : E(e)), void 0 !== L)) return L;
          if (!O(e)) return e;
          var N = g(e);
          if (N) {
            if (((L = v(e)), !D)) return u(e, L);
          } else {
            var W = h(e),
              F = W == j || "[object GeneratorFunction]" == W;
            if (b(e)) return l(e, D);
            if (W == k || W == A || (F && !T)) {
              if (((L = I || F ? {} : m(e)), !D))
                return I ? f(e, c(L, e)) : s(e, i(L, e));
            } else {
              if (!P[W]) return T ? e : {};
              L = y(e, W, D);
            }
          }
          _ || (_ = new r());
          var z = _.get(e);
          if (z) return z;
          _.set(e, L),
            w(e)
              ? e.forEach(function (r) {
                  L.add(t(r, n, E, r, e, _));
                })
              : x(e) &&
                e.forEach(function (r, o) {
                  L.set(o, t(r, n, E, o, e, _));
                });
          var U = N ? void 0 : (R ? (I ? d : p) : I ? S : C)(e);
          return (
            o(U || e, function (r, o) {
              U && (r = e[(o = r)]), a(L, o, t(r, n, E, o, e, _));
            }),
            L
          );
        });
    },
    21468: (t, e, n) => {
      var r = n(20692),
        o = n(59055),
        a = n(32683),
        i = n(68950),
        c = n(16194),
        l = n(60075);
      t.exports = function (t, e, n, u) {
        var s = -1,
          f = o,
          p = !0,
          d = t.length,
          h = [],
          v = e.length;
        if (!d) return h;
        n && (e = i(e, c(n))),
          u
            ? ((f = a), (p = !1))
            : e.length >= 200 && ((f = l), (p = !1), (e = new r(e)));
        t: for (; ++s < d; ) {
          var y = t[s],
            m = null == n ? y : n(y);
          if (((y = u || 0 !== y ? y : 0), p && m === m)) {
            for (var g = v; g--; ) if (e[g] === m) continue t;
            h.push(y);
          } else f(e, m, u) || h.push(y);
        }
        return h;
      };
    },
    87927: (t, e, n) => {
      var r = n(15358),
        o = n(67056)(r);
      t.exports = o;
    },
    2045: (t) => {
      t.exports = function (t, e, n, r) {
        for (var o = t.length, a = n + (r ? 1 : -1); r ? a-- : ++a < o; )
          if (e(t[a], a, t)) return a;
        return -1;
      };
    },
    55182: (t, e, n) => {
      var r = n(41705),
        o = n(73529);
      t.exports = function t(e, n, a, i, c) {
        var l = -1,
          u = e.length;
        for (a || (a = o), c || (c = []); ++l < u; ) {
          var s = e[l];
          n > 0 && a(s)
            ? n > 1
              ? t(s, n - 1, a, i, c)
              : r(c, s)
            : i || (c[c.length] = s);
        }
        return c;
      };
    },
    15358: (t, e, n) => {
      var r = n(85099),
        o = n(12742);
      t.exports = function (t, e) {
        return t && r(t, e, o);
      };
    },
    98667: (t, e, n) => {
      var r = n(43082),
        o = n(69793);
      t.exports = function (t, e) {
        for (var n = 0, a = (e = r(e, t)).length; null != t && n < a; )
          t = t[o(e[n++])];
        return n && n == a ? t : void 0;
      };
    },
    61986: (t, e, n) => {
      var r = n(41705),
        o = n(93629);
      t.exports = function (t, e, n) {
        var a = e(t);
        return o(t) ? a : r(a, n(t));
      };
    },
    90529: (t) => {
      t.exports = function (t, e) {
        return null != t && e in Object(t);
      };
    },
    24842: (t, e, n) => {
      var r = n(2045),
        o = n(50505),
        a = n(77167);
      t.exports = function (t, e, n) {
        return e === e ? a(t, e, n) : r(t, o, n);
      };
    },
    67162: (t, e, n) => {
      var r = n(15358);
      t.exports = function (t, e, n, o) {
        return (
          r(t, function (t, r, a) {
            e(o, n(t), r, a);
          }),
          o
        );
      };
    },
    89931: (t, e, n) => {
      var r = n(39066),
        o = n(43141);
      t.exports = function (t) {
        return o(t) && "[object Date]" == r(t);
      };
    },
    71848: (t, e, n) => {
      var r = n(93355),
        o = n(43141);
      t.exports = function t(e, n, a, i, c) {
        return (
          e === n ||
          (null == e || null == n || (!o(e) && !o(n))
            ? e !== e && n !== n
            : r(e, n, a, i, t, c))
        );
      };
    },
    93355: (t, e, n) => {
      var r = n(22854),
        o = n(15305),
        a = n(92206),
        i = n(88078),
        c = n(88383),
        l = n(93629),
        u = n(5174),
        s = n(19102),
        f = "[object Arguments]",
        p = "[object Array]",
        d = "[object Object]",
        h = Object.prototype.hasOwnProperty;
      t.exports = function (t, e, n, v, y, m) {
        var g = l(t),
          b = l(e),
          x = g ? p : c(t),
          O = b ? p : c(e),
          w = (x = x == f ? d : x) == d,
          C = (O = O == f ? d : O) == d,
          S = x == O;
        if (S && u(t)) {
          if (!u(e)) return !1;
          (g = !0), (w = !1);
        }
        if (S && !w)
          return (
            m || (m = new r()),
            g || s(t) ? o(t, e, n, v, y, m) : a(t, e, x, n, v, y, m)
          );
        if (!(1 & n)) {
          var A = w && h.call(t, "__wrapped__"),
            j = C && h.call(e, "__wrapped__");
          if (A || j) {
            var k = A ? t.value() : t,
              P = j ? e.value() : e;
            return m || (m = new r()), y(k, P, n, v, m);
          }
        }
        return !!S && (m || (m = new r()), i(t, e, n, v, y, m));
      };
    },
    53085: (t, e, n) => {
      var r = n(88383),
        o = n(43141);
      t.exports = function (t) {
        return o(t) && "[object Map]" == r(t);
      };
    },
    8856: (t, e, n) => {
      var r = n(22854),
        o = n(71848);
      t.exports = function (t, e, n, a) {
        var i = n.length,
          c = i,
          l = !a;
        if (null == t) return !c;
        for (t = Object(t); i--; ) {
          var u = n[i];
          if (l && u[2] ? u[1] !== t[u[0]] : !(u[0] in t)) return !1;
        }
        for (; ++i < c; ) {
          var s = (u = n[i])[0],
            f = t[s],
            p = u[1];
          if (l && u[2]) {
            if (void 0 === f && !(s in t)) return !1;
          } else {
            var d = new r();
            if (a) var h = a(f, p, s, t, e, d);
            if (!(void 0 === h ? o(p, f, 3, a, d) : h)) return !1;
          }
        }
        return !0;
      };
    },
    50505: (t) => {
      t.exports = function (t) {
        return t !== t;
      };
    },
    57817: (t, e, n) => {
      var r = n(39066),
        o = n(43141);
      t.exports = function (t) {
        return o(t) && "[object RegExp]" == r(t);
      };
    },
    48680: (t, e, n) => {
      var r = n(88383),
        o = n(43141);
      t.exports = function (t) {
        return o(t) && "[object Set]" == r(t);
      };
    },
    56025: (t, e, n) => {
      var r = n(97080),
        o = n(24322),
        a = n(2100),
        i = n(93629),
        c = n(10038);
      t.exports = function (t) {
        return "function" == typeof t
          ? t
          : null == t
            ? a
            : "object" == typeof t
              ? i(t)
                ? o(t[0], t[1])
                : r(t)
              : c(t);
      };
    },
    43654: (t, e, n) => {
      var r = n(62936),
        o = n(75964),
        a = Object.prototype.hasOwnProperty;
      t.exports = function (t) {
        if (!r(t)) return o(t);
        var e = [];
        for (var n in Object(t))
          a.call(t, n) && "constructor" != n && e.push(n);
        return e;
      };
    },
    53849: (t, e, n) => {
      var r = n(87927),
        o = n(21473);
      t.exports = function (t, e) {
        var n = -1,
          a = o(t) ? Array(t.length) : [];
        return (
          r(t, function (t, r, o) {
            a[++n] = e(t, r, o);
          }),
          a
        );
      };
    },
    97080: (t, e, n) => {
      var r = n(8856),
        o = n(79091),
        a = n(50284);
      t.exports = function (t) {
        var e = o(t);
        return 1 == e.length && e[0][2]
          ? a(e[0][0], e[0][1])
          : function (n) {
              return n === t || r(n, t, e);
            };
      };
    },
    24322: (t, e, n) => {
      var r = n(71848),
        o = n(26181),
        a = n(75658),
        i = n(25823),
        c = n(25072),
        l = n(50284),
        u = n(69793);
      t.exports = function (t, e) {
        return i(t) && c(e)
          ? l(u(t), e)
          : function (n) {
              var i = o(n, t);
              return void 0 === i && i === e ? a(n, t) : r(e, i, 3);
            };
      };
    },
    93226: (t, e, n) => {
      var r = n(68950),
        o = n(98667),
        a = n(56025),
        i = n(53849),
        c = n(19179),
        l = n(16194),
        u = n(94480),
        s = n(2100),
        f = n(93629);
      t.exports = function (t, e, n) {
        e = e.length
          ? r(e, function (t) {
              return f(t)
                ? function (e) {
                    return o(e, 1 === t.length ? t[0] : t);
                  }
                : t;
            })
          : [s];
        var p = -1;
        e = r(e, l(a));
        var d = i(t, function (t, n, o) {
          return {
            criteria: r(e, function (e) {
              return e(t);
            }),
            index: ++p,
            value: t,
          };
        });
        return c(d, function (t, e) {
          return u(t, e, n);
        });
      };
    },
    14980: (t, e, n) => {
      var r = n(2591),
        o = n(75658);
      t.exports = function (t, e) {
        return r(t, e, function (e, n) {
          return o(t, n);
        });
      };
    },
    2591: (t, e, n) => {
      var r = n(98667),
        o = n(40379),
        a = n(43082);
      t.exports = function (t, e, n) {
        for (var i = -1, c = e.length, l = {}; ++i < c; ) {
          var u = e[i],
            s = r(t, u);
          n(s, u) && o(l, a(u, t), s);
        }
        return l;
      };
    },
    9586: (t) => {
      t.exports = function (t) {
        return function (e) {
          return null == e ? void 0 : e[t];
        };
      };
    },
    4084: (t, e, n) => {
      var r = n(98667);
      t.exports = function (t) {
        return function (e) {
          return r(e, t);
        };
      };
    },
    7255: (t) => {
      var e = Math.ceil,
        n = Math.max;
      t.exports = function (t, r, o, a) {
        for (var i = -1, c = n(e((r - t) / (o || 1)), 0), l = Array(c); c--; )
          (l[a ? c : ++i] = t), (t += o);
        return l;
      };
    },
    40379: (t, e, n) => {
      var r = n(18463),
        o = n(43082),
        a = n(26800),
        i = n(8092),
        c = n(69793);
      t.exports = function (t, e, n, l) {
        if (!i(t)) return t;
        for (
          var u = -1, s = (e = o(e, t)).length, f = s - 1, p = t;
          null != p && ++u < s;

        ) {
          var d = c(e[u]),
            h = n;
          if ("__proto__" === d || "constructor" === d || "prototype" === d)
            return t;
          if (u != f) {
            var v = p[d];
            void 0 === (h = l ? l(v, d, p) : void 0) &&
              (h = i(v) ? v : a(e[u + 1]) ? [] : {});
          }
          r(p, d, h), (p = p[d]);
        }
        return t;
      };
    },
    59204: (t, e, n) => {
      var r = n(87927);
      t.exports = function (t, e) {
        var n;
        return (
          r(t, function (t, r, o) {
            return !(n = e(t, r, o));
          }),
          !!n
        );
      };
    },
    19179: (t) => {
      t.exports = function (t, e) {
        var n = t.length;
        for (t.sort(e); n--; ) t[n] = t[n].value;
        return t;
      };
    },
    75261: (t, e, n) => {
      var r = n(29231);
      t.exports = function (t, e) {
        for (var n = -1, o = t.length, a = 0, i = []; ++n < o; ) {
          var c = t[n],
            l = e ? e(c) : c;
          if (!n || !r(l, u)) {
            var u = l;
            i[a++] = 0 === c ? 0 : c;
          }
        }
        return i;
      };
    },
    58645: (t) => {
      t.exports = function (t, e) {
        for (var n, r = -1, o = t.length; ++r < o; ) {
          var a = e(t[r]);
          void 0 !== a && (n = void 0 === n ? a : n + a);
        }
        return n;
      };
    },
    2446: (t, e, n) => {
      var r = n(87197),
        o = n(68950),
        a = n(93629),
        i = n(70152),
        c = r ? r.prototype : void 0,
        l = c ? c.toString : void 0;
      t.exports = function t(e) {
        if ("string" == typeof e) return e;
        if (a(e)) return o(e, t) + "";
        if (i(e)) return l ? l.call(e) : "";
        var n = e + "";
        return "0" == n && 1 / e == -Infinity ? "-0" : n;
      };
    },
    20821: (t, e, n) => {
      var r = n(26050),
        o = /^\s+/;
      t.exports = function (t) {
        return t ? t.slice(0, r(t) + 1).replace(o, "") : t;
      };
    },
    39602: (t, e, n) => {
      var r = n(20692),
        o = n(59055),
        a = n(32683),
        i = n(60075),
        c = n(77730),
        l = n(22230);
      t.exports = function (t, e, n) {
        var u = -1,
          s = o,
          f = t.length,
          p = !0,
          d = [],
          h = d;
        if (n) (p = !1), (s = a);
        else if (f >= 200) {
          var v = e ? null : c(t);
          if (v) return l(v);
          (p = !1), (s = i), (h = new r());
        } else h = e ? [] : d;
        t: for (; ++u < f; ) {
          var y = t[u],
            m = e ? e(y) : y;
          if (((y = n || 0 !== y ? y : 0), p && m === m)) {
            for (var g = h.length; g--; ) if (h[g] === m) continue t;
            e && h.push(m), d.push(y);
          } else s(h, m, n) || (h !== d && h.push(m), d.push(y));
        }
        return d;
      };
    },
    28019: (t, e, n) => {
      var r = n(68950);
      t.exports = function (t, e) {
        return r(e, function (e) {
          return t[e];
        });
      };
    },
    60075: (t) => {
      t.exports = function (t, e) {
        return t.has(e);
      };
    },
    43082: (t, e, n) => {
      var r = n(93629),
        o = n(25823),
        a = n(10170),
        i = n(63518);
      t.exports = function (t, e) {
        return r(t) ? t : o(t, e) ? [t] : a(i(t));
      };
    },
    61022: (t, e, n) => {
      var r = n(7010);
      t.exports = function (t, e) {
        var n = e ? r(t.buffer) : t.buffer;
        return new t.constructor(n, t.byteOffset, t.byteLength);
      };
    },
    18503: (t) => {
      var e = /\w*$/;
      t.exports = function (t) {
        var n = new t.constructor(t.source, e.exec(t));
        return (n.lastIndex = t.lastIndex), n;
      };
    },
    64720: (t, e, n) => {
      var r = n(87197),
        o = r ? r.prototype : void 0,
        a = o ? o.valueOf : void 0;
      t.exports = function (t) {
        return a ? Object(a.call(t)) : {};
      };
    },
    88558: (t, e, n) => {
      var r = n(70152);
      t.exports = function (t, e) {
        if (t !== e) {
          var n = void 0 !== t,
            o = null === t,
            a = t === t,
            i = r(t),
            c = void 0 !== e,
            l = null === e,
            u = e === e,
            s = r(e);
          if (
            (!l && !s && !i && t > e) ||
            (i && c && u && !l && !s) ||
            (o && c && u) ||
            (!n && u) ||
            !a
          )
            return 1;
          if (
            (!o && !i && !s && t < e) ||
            (s && n && a && !o && !i) ||
            (l && n && a) ||
            (!c && a) ||
            !u
          )
            return -1;
        }
        return 0;
      };
    },
    94480: (t, e, n) => {
      var r = n(88558);
      t.exports = function (t, e, n) {
        for (
          var o = -1,
            a = t.criteria,
            i = e.criteria,
            c = a.length,
            l = n.length;
          ++o < c;

        ) {
          var u = r(a[o], i[o]);
          if (u) return o >= l ? u : u * ("desc" == n[o] ? -1 : 1);
        }
        return t.index - e.index;
      };
    },
    52455: (t, e, n) => {
      var r = n(64503),
        o = n(65918);
      t.exports = function (t, e) {
        return r(t, o(t), e);
      };
    },
    57636: (t, e, n) => {
      var r = n(64503),
        o = n(38487);
      t.exports = function (t, e) {
        return r(t, o(t), e);
      };
    },
    74629: (t, e, n) => {
      var r = n(31211),
        o = n(38430),
        a = n(56025),
        i = n(93629);
      t.exports = function (t, e) {
        return function (n, c) {
          var l = i(n) ? r : o,
            u = e ? e() : {};
          return l(n, t, a(c, 2), u);
        };
      };
    },
    67056: (t, e, n) => {
      var r = n(21473);
      t.exports = function (t, e) {
        return function (n, o) {
          if (null == n) return n;
          if (!r(n)) return t(n, o);
          for (
            var a = n.length, i = e ? a : -1, c = Object(n);
            (e ? i-- : ++i < a) && !1 !== o(c[i], i, c);

          );
          return n;
        };
      };
    },
    95481: (t, e, n) => {
      var r = n(56025),
        o = n(21473),
        a = n(12742);
      t.exports = function (t) {
        return function (e, n, i) {
          var c = Object(e);
          if (!o(e)) {
            var l = r(n, 3);
            (e = a(e)),
              (n = function (t) {
                return l(c[t], t, c);
              });
          }
          var u = t(e, n, i);
          return u > -1 ? c[l ? e[u] : u] : void 0;
        };
      };
    },
    60164: (t, e, n) => {
      var r = n(67162);
      t.exports = function (t, e) {
        return function (n, o) {
          return r(n, t, e(o), {});
        };
      };
    },
    56381: (t, e, n) => {
      var r = n(7255),
        o = n(3195),
        a = n(91495);
      t.exports = function (t) {
        return function (e, n, i) {
          return (
            i && "number" != typeof i && o(e, n, i) && (n = i = void 0),
            (e = a(e)),
            void 0 === n ? ((n = e), (e = 0)) : (n = a(n)),
            (i = void 0 === i ? (e < n ? 1 : -1) : a(i)),
            r(e, n, i, t)
          );
        };
      };
    },
    77730: (t, e, n) => {
      var r = n(23924),
        o = n(19694),
        a = n(22230),
        i =
          r && 1 / a(new r([, -0]))[1] == 1 / 0
            ? function (t) {
                return new r(t);
              }
            : o;
      t.exports = i;
    },
    15305: (t, e, n) => {
      var r = n(20692),
        o = n(47897),
        a = n(60075);
      t.exports = function (t, e, n, i, c, l) {
        var u = 1 & n,
          s = t.length,
          f = e.length;
        if (s != f && !(u && f > s)) return !1;
        var p = l.get(t),
          d = l.get(e);
        if (p && d) return p == e && d == t;
        var h = -1,
          v = !0,
          y = 2 & n ? new r() : void 0;
        for (l.set(t, e), l.set(e, t); ++h < s; ) {
          var m = t[h],
            g = e[h];
          if (i) var b = u ? i(g, m, h, e, t, l) : i(m, g, h, t, e, l);
          if (void 0 !== b) {
            if (b) continue;
            v = !1;
            break;
          }
          if (y) {
            if (
              !o(e, function (t, e) {
                if (!a(y, e) && (m === t || c(m, t, n, i, l))) return y.push(e);
              })
            ) {
              v = !1;
              break;
            }
          } else if (m !== g && !c(m, g, n, i, l)) {
            v = !1;
            break;
          }
        }
        return l.delete(t), l.delete(e), v;
      };
    },
    92206: (t, e, n) => {
      var r = n(87197),
        o = n(46219),
        a = n(29231),
        i = n(15305),
        c = n(90234),
        l = n(22230),
        u = r ? r.prototype : void 0,
        s = u ? u.valueOf : void 0;
      t.exports = function (t, e, n, r, u, f, p) {
        switch (n) {
          case "[object DataView]":
            if (t.byteLength != e.byteLength || t.byteOffset != e.byteOffset)
              return !1;
            (t = t.buffer), (e = e.buffer);
          case "[object ArrayBuffer]":
            return !(t.byteLength != e.byteLength || !f(new o(t), new o(e)));
          case "[object Boolean]":
          case "[object Date]":
          case "[object Number]":
            return a(+t, +e);
          case "[object Error]":
            return t.name == e.name && t.message == e.message;
          case "[object RegExp]":
          case "[object String]":
            return t == e + "";
          case "[object Map]":
            var d = c;
          case "[object Set]":
            var h = 1 & r;
            if ((d || (d = l), t.size != e.size && !h)) return !1;
            var v = p.get(t);
            if (v) return v == e;
            (r |= 2), p.set(t, e);
            var y = i(d(t), d(e), r, u, f, p);
            return p.delete(t), y;
          case "[object Symbol]":
            if (s) return s.call(t) == s.call(e);
        }
        return !1;
      };
    },
    88078: (t, e, n) => {
      var r = n(38248),
        o = Object.prototype.hasOwnProperty;
      t.exports = function (t, e, n, a, i, c) {
        var l = 1 & n,
          u = r(t),
          s = u.length;
        if (s != r(e).length && !l) return !1;
        for (var f = s; f--; ) {
          var p = u[f];
          if (!(l ? p in e : o.call(e, p))) return !1;
        }
        var d = c.get(t),
          h = c.get(e);
        if (d && h) return d == e && h == t;
        var v = !0;
        c.set(t, e), c.set(e, t);
        for (var y = l; ++f < s; ) {
          var m = t[(p = u[f])],
            g = e[p];
          if (a) var b = l ? a(g, m, p, e, t, c) : a(m, g, p, t, e, c);
          if (!(void 0 === b ? m === g || i(m, g, n, a, c) : b)) {
            v = !1;
            break;
          }
          y || (y = "constructor" == p);
        }
        if (v && !y) {
          var x = t.constructor,
            O = e.constructor;
          x == O ||
            !("constructor" in t) ||
            !("constructor" in e) ||
            ("function" == typeof x &&
              x instanceof x &&
              "function" == typeof O &&
              O instanceof O) ||
            (v = !1);
        }
        return c.delete(t), c.delete(e), v;
      };
    },
    27038: (t, e, n) => {
      var r = n(25506),
        o = n(64262),
        a = n(79156);
      t.exports = function (t) {
        return a(o(t, void 0, r), t + "");
      };
    },
    38248: (t, e, n) => {
      var r = n(61986),
        o = n(65918),
        a = n(12742);
      t.exports = function (t) {
        return r(t, a, o);
      };
    },
    55341: (t, e, n) => {
      var r = n(61986),
        o = n(38487),
        a = n(73961);
      t.exports = function (t) {
        return r(t, a, o);
      };
    },
    79091: (t, e, n) => {
      var r = n(25072),
        o = n(12742);
      t.exports = function (t) {
        for (var e = o(t), n = e.length; n--; ) {
          var a = e[n],
            i = t[a];
          e[n] = [a, i, r(i)];
        }
        return e;
      };
    },
    65918: (t, e, n) => {
      var r = n(84903),
        o = n(68174),
        a = Object.prototype.propertyIsEnumerable,
        i = Object.getOwnPropertySymbols,
        c = i
          ? function (t) {
              return null == t
                ? []
                : ((t = Object(t)),
                  r(i(t), function (e) {
                    return a.call(t, e);
                  }));
            }
          : o;
      t.exports = c;
    },
    38487: (t, e, n) => {
      var r = n(41705),
        o = n(31137),
        a = n(65918),
        i = n(68174),
        c = Object.getOwnPropertySymbols
          ? function (t) {
              for (var e = []; t; ) r(e, a(t)), (t = o(t));
              return e;
            }
          : i;
      t.exports = c;
    },
    88383: (t, e, n) => {
      var r = n(50908),
        o = n(95797),
        a = n(78319),
        i = n(23924),
        c = n(7091),
        l = n(39066),
        u = n(27907),
        s = "[object Map]",
        f = "[object Promise]",
        p = "[object Set]",
        d = "[object WeakMap]",
        h = "[object DataView]",
        v = u(r),
        y = u(o),
        m = u(a),
        g = u(i),
        b = u(c),
        x = l;
      ((r && x(new r(new ArrayBuffer(1))) != h) ||
        (o && x(new o()) != s) ||
        (a && x(a.resolve()) != f) ||
        (i && x(new i()) != p) ||
        (c && x(new c()) != d)) &&
        (x = function (t) {
          var e = l(t),
            n = "[object Object]" == e ? t.constructor : void 0,
            r = n ? u(n) : "";
          if (r)
            switch (r) {
              case v:
                return h;
              case y:
                return s;
              case m:
                return f;
              case g:
                return p;
              case b:
                return d;
            }
          return e;
        }),
        (t.exports = x);
    },
    86417: (t, e, n) => {
      var r = n(43082),
        o = n(34963),
        a = n(93629),
        i = n(26800),
        c = n(24635),
        l = n(69793);
      t.exports = function (t, e, n) {
        for (var u = -1, s = (e = r(e, t)).length, f = !1; ++u < s; ) {
          var p = l(e[u]);
          if (!(f = null != t && n(t, p))) break;
          t = t[p];
        }
        return f || ++u != s
          ? f
          : !!(s = null == t ? 0 : t.length) &&
              c(s) &&
              i(p, s) &&
              (a(t) || o(t));
      };
    },
    39243: (t) => {
      var e = Object.prototype.hasOwnProperty;
      t.exports = function (t) {
        var n = t.length,
          r = new t.constructor(n);
        return (
          n &&
            "string" == typeof t[0] &&
            e.call(t, "index") &&
            ((r.index = t.index), (r.input = t.input)),
          r
        );
      };
    },
    39759: (t, e, n) => {
      var r = n(7010),
        o = n(61022),
        a = n(18503),
        i = n(64720),
        c = n(40613);
      t.exports = function (t, e, n) {
        var l = t.constructor;
        switch (e) {
          case "[object ArrayBuffer]":
            return r(t);
          case "[object Boolean]":
          case "[object Date]":
            return new l(+t);
          case "[object DataView]":
            return o(t, n);
          case "[object Float32Array]":
          case "[object Float64Array]":
          case "[object Int8Array]":
          case "[object Int16Array]":
          case "[object Int32Array]":
          case "[object Uint8Array]":
          case "[object Uint8ClampedArray]":
          case "[object Uint16Array]":
          case "[object Uint32Array]":
            return c(t, n);
          case "[object Map]":
          case "[object Set]":
            return new l();
          case "[object Number]":
          case "[object String]":
            return new l(t);
          case "[object RegExp]":
            return a(t);
          case "[object Symbol]":
            return i(t);
        }
      };
    },
    73529: (t, e, n) => {
      var r = n(87197),
        o = n(34963),
        a = n(93629),
        i = r ? r.isConcatSpreadable : void 0;
      t.exports = function (t) {
        return a(t) || o(t) || !!(i && t && t[i]);
      };
    },
    25823: (t, e, n) => {
      var r = n(93629),
        o = n(70152),
        a = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/,
        i = /^\w*$/;
      t.exports = function (t, e) {
        if (r(t)) return !1;
        var n = typeof t;
        return (
          !(
            "number" != n &&
            "symbol" != n &&
            "boolean" != n &&
            null != t &&
            !o(t)
          ) ||
          i.test(t) ||
          !a.test(t) ||
          (null != e && t in Object(e))
        );
      };
    },
    25072: (t, e, n) => {
      var r = n(8092);
      t.exports = function (t) {
        return t === t && !r(t);
      };
    },
    90234: (t) => {
      t.exports = function (t) {
        var e = -1,
          n = Array(t.size);
        return (
          t.forEach(function (t, r) {
            n[++e] = [r, t];
          }),
          n
        );
      };
    },
    50284: (t) => {
      t.exports = function (t, e) {
        return function (n) {
          return null != n && n[t] === e && (void 0 !== e || t in Object(n));
        };
      };
    },
    14634: (t, e, n) => {
      var r = n(49151);
      t.exports = function (t) {
        var e = r(t, function (t) {
            return 500 === n.size && n.clear(), t;
          }),
          n = e.cache;
        return e;
      };
    },
    75964: (t, e, n) => {
      var r = n(12709)(Object.keys, Object);
      t.exports = r;
    },
    35774: (t) => {
      t.exports = function (t) {
        return this.__data__.set(t, "__lodash_hash_undefined__"), this;
      };
    },
    41596: (t) => {
      t.exports = function (t) {
        return this.__data__.has(t);
      };
    },
    22230: (t) => {
      t.exports = function (t) {
        var e = -1,
          n = Array(t.size);
        return (
          t.forEach(function (t) {
            n[++e] = t;
          }),
          n
        );
      };
    },
    77167: (t) => {
      t.exports = function (t, e, n) {
        for (var r = n - 1, o = t.length; ++r < o; ) if (t[r] === e) return r;
        return -1;
      };
    },
    10170: (t, e, n) => {
      var r = n(14634),
        o =
          /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g,
        a = /\\(\\)?/g,
        i = r(function (t) {
          var e = [];
          return (
            46 === t.charCodeAt(0) && e.push(""),
            t.replace(o, function (t, n, r, o) {
              e.push(r ? o.replace(a, "$1") : n || t);
            }),
            e
          );
        });
      t.exports = i;
    },
    69793: (t, e, n) => {
      var r = n(70152);
      t.exports = function (t) {
        if ("string" == typeof t || r(t)) return t;
        var e = t + "";
        return "0" == e && 1 / t == -Infinity ? "-0" : e;
      };
    },
    26050: (t) => {
      var e = /\s/;
      t.exports = function (t) {
        for (var n = t.length; n-- && e.test(t.charAt(n)); );
        return n;
      };
    },
    15687: (t, e, n) => {
      var r = n(18463),
        o = n(64503),
        a = n(39934),
        i = n(21473),
        c = n(62936),
        l = n(12742),
        u = Object.prototype.hasOwnProperty,
        s = a(function (t, e) {
          if (c(e) || i(e)) o(e, l(e), t);
          else for (var n in e) u.call(e, n) && r(t, n, e[n]);
        });
      t.exports = s;
    },
    58121: (t, e, n) => {
      var r = n(31905);
      t.exports = function (t) {
        return r(t, 5);
      };
    },
    66933: (t, e, n) => {
      var r = n(58794),
        o = n(29231),
        a = n(3195),
        i = n(73961),
        c = Object.prototype,
        l = c.hasOwnProperty,
        u = r(function (t, e) {
          t = Object(t);
          var n = -1,
            r = e.length,
            u = r > 2 ? e[2] : void 0;
          for (u && a(e[0], e[1], u) && (r = 1); ++n < r; )
            for (var s = e[n], f = i(s), p = -1, d = f.length; ++p < d; ) {
              var h = f[p],
                v = t[h];
              (void 0 === v || (o(v, c[h]) && !l.call(t, h))) && (t[h] = s[h]);
            }
          return t;
        });
      t.exports = u;
    },
    71180: (t, e, n) => {
      var r = n(21468),
        o = n(55182),
        a = n(58794),
        i = n(56279),
        c = a(function (t, e) {
          return i(t) ? r(t, o(e, 1, i, !0)) : [];
        });
      t.exports = c;
    },
    61211: (t, e, n) => {
      var r = n(95481)(n(51475));
      t.exports = r;
    },
    51475: (t, e, n) => {
      var r = n(2045),
        o = n(56025),
        a = n(39753),
        i = Math.max;
      t.exports = function (t, e, n) {
        var c = null == t ? 0 : t.length;
        if (!c) return -1;
        var l = null == n ? 0 : a(n);
        return l < 0 && (l = i(c + l, 0)), r(t, o(e, 3), l);
      };
    },
    25506: (t, e, n) => {
      var r = n(55182);
      t.exports = function (t) {
        return (null == t ? 0 : t.length) ? r(t, 1) : [];
      };
    },
    99305: (t) => {
      t.exports = function (t) {
        for (var e = -1, n = null == t ? 0 : t.length, r = {}; ++e < n; ) {
          var o = t[e];
          r[o[0]] = o[1];
        }
        return r;
      };
    },
    26181: (t, e, n) => {
      var r = n(98667);
      t.exports = function (t, e, n) {
        var o = null == t ? void 0 : r(t, e);
        return void 0 === o ? n : o;
      };
    },
    98444: (t, e, n) => {
      var r = n(32526),
        o = n(74629),
        a = Object.prototype.hasOwnProperty,
        i = o(function (t, e, n) {
          a.call(t, n) ? t[n].push(e) : r(t, n, [e]);
        });
      t.exports = i;
    },
    75658: (t, e, n) => {
      var r = n(90529),
        o = n(86417);
      t.exports = function (t, e) {
        return null != t && o(t, e, r);
      };
    },
    40806: (t, e, n) => {
      var r = n(24842),
        o = n(21473),
        a = n(26769),
        i = n(39753),
        c = n(92063),
        l = Math.max;
      t.exports = function (t, e, n, u) {
        (t = o(t) ? t : c(t)), (n = n && !u ? i(n) : 0);
        var s = t.length;
        return (
          n < 0 && (n = l(s + n, 0)),
          a(t) ? n <= s && t.indexOf(e, n) > -1 : !!s && r(t, e, n) > -1
        );
      };
    },
    65417: (t, e, n) => {
      var r = n(71547),
        o = n(60164),
        a = n(2100),
        i = Object.prototype.toString,
        c = o(function (t, e, n) {
          null != e && "function" != typeof e.toString && (e = i.call(e)),
            (t[e] = n);
        }, r(a));
      t.exports = c;
    },
    36609: (t, e, n) => {
      var r = n(89931),
        o = n(16194),
        a = n(49494),
        i = a && a.isDate,
        c = i ? o(i) : r;
      t.exports = c;
    },
    66364: (t, e, n) => {
      var r = n(43654),
        o = n(88383),
        a = n(34963),
        i = n(93629),
        c = n(21473),
        l = n(5174),
        u = n(62936),
        s = n(19102),
        f = Object.prototype.hasOwnProperty;
      t.exports = function (t) {
        if (null == t) return !0;
        if (
          c(t) &&
          (i(t) ||
            "string" == typeof t ||
            "function" == typeof t.splice ||
            l(t) ||
            s(t) ||
            a(t))
        )
          return !t.length;
        var e = o(t);
        if ("[object Map]" == e || "[object Set]" == e) return !t.size;
        if (u(t)) return !r(t).length;
        for (var n in t) if (f.call(t, n)) return !1;
        return !0;
      };
    },
    18111: (t, e, n) => {
      var r = n(71848);
      t.exports = function (t, e) {
        return r(t, e);
      };
    },
    60103: (t, e, n) => {
      var r = n(53085),
        o = n(16194),
        a = n(49494),
        i = a && a.isMap,
        c = i ? o(i) : r;
      t.exports = c;
    },
    42854: (t) => {
      t.exports = function (t) {
        return null == t;
      };
    },
    65625: (t, e, n) => {
      var r = n(57817),
        o = n(16194),
        a = n(49494),
        i = a && a.isRegExp,
        c = i ? o(i) : r;
      t.exports = c;
    },
    36995: (t, e, n) => {
      var r = n(48680),
        o = n(16194),
        a = n(49494),
        i = a && a.isSet,
        c = i ? o(i) : r;
      t.exports = c;
    },
    26769: (t, e, n) => {
      var r = n(39066),
        o = n(93629),
        a = n(43141);
      t.exports = function (t) {
        return (
          "string" == typeof t || (!o(t) && a(t) && "[object String]" == r(t))
        );
      };
    },
    70152: (t, e, n) => {
      var r = n(39066),
        o = n(43141);
      t.exports = function (t) {
        return "symbol" == typeof t || (o(t) && "[object Symbol]" == r(t));
      };
    },
    42530: (t) => {
      t.exports = function (t) {
        return void 0 === t;
      };
    },
    12742: (t, e, n) => {
      var r = n(47538),
        o = n(43654),
        a = n(21473);
      t.exports = function (t) {
        return a(t) ? r(t) : o(t);
      };
    },
    15727: (t) => {
      t.exports = function (t) {
        var e = null == t ? 0 : t.length;
        return e ? t[e - 1] : void 0;
      };
    },
    49151: (t, e, n) => {
      var r = n(78059);
      function o(t, e) {
        if ("function" != typeof t || (null != e && "function" != typeof e))
          throw new TypeError("Expected a function");
        var n = function () {
          var r = arguments,
            o = e ? e.apply(this, r) : r[0],
            a = n.cache;
          if (a.has(o)) return a.get(o);
          var i = t.apply(this, r);
          return (n.cache = a.set(o, i) || a), i;
        };
        return (n.cache = new (o.Cache || r)()), n;
      }
      (o.Cache = r), (t.exports = o);
    },
    79286: (t, e, n) => {
      var r = n(64173),
        o = n(39934)(function (t, e, n) {
          r(t, e, n);
        });
      t.exports = o;
    },
    56754: (t) => {
      t.exports = function (t) {
        if ("function" != typeof t) throw new TypeError("Expected a function");
        return function () {
          var e = arguments;
          switch (e.length) {
            case 0:
              return !t.call(this);
            case 1:
              return !t.call(this, e[0]);
            case 2:
              return !t.call(this, e[0], e[1]);
            case 3:
              return !t.call(this, e[0], e[1], e[2]);
          }
          return !t.apply(this, e);
        };
      };
    },
    19694: (t) => {
      t.exports = function () {};
    },
    64417: (t, e, n) => {
      var r = n(56025),
        o = n(56754),
        a = n(87790);
      t.exports = function (t, e) {
        return a(t, o(r(e)));
      };
    },
    45812: (t, e, n) => {
      var r = n(93226),
        o = n(93629);
      t.exports = function (t, e, n, a) {
        return null == t
          ? []
          : (o(e) || (e = null == e ? [] : [e]),
            o((n = a ? void 0 : n)) || (n = null == n ? [] : [n]),
            r(t, e, n));
      };
    },
    36460: (t, e, n) => {
      var r = n(14980),
        o = n(27038)(function (t, e) {
          return null == t ? {} : r(t, e);
        });
      t.exports = o;
    },
    87790: (t, e, n) => {
      var r = n(68950),
        o = n(56025),
        a = n(2591),
        i = n(55341);
      t.exports = function (t, e) {
        if (null == t) return {};
        var n = r(i(t), function (t) {
          return [t];
        });
        return (
          (e = o(e)),
          a(t, n, function (t, n) {
            return e(t, n[0]);
          })
        );
      };
    },
    10038: (t, e, n) => {
      var r = n(9586),
        o = n(4084),
        a = n(25823),
        i = n(69793);
      t.exports = function (t) {
        return a(t) ? r(i(t)) : o(t);
      };
    },
    66222: (t, e, n) => {
      var r = n(56381)();
      t.exports = r;
    },
    14064: (t, e, n) => {
      var r = n(47897),
        o = n(56025),
        a = n(59204),
        i = n(93629),
        c = n(3195);
      t.exports = function (t, e, n) {
        var l = i(t) ? r : a;
        return n && c(t, e, n) && (e = void 0), l(t, o(e, 3));
      };
    },
    21139: (t, e, n) => {
      var r = n(75261);
      t.exports = function (t) {
        return t && t.length ? r(t) : [];
      };
    },
    68174: (t) => {
      t.exports = function () {
        return [];
      };
    },
    87151: (t, e, n) => {
      var r = n(58645),
        o = n(2100);
      t.exports = function (t) {
        return t && t.length ? r(t, o) : 0;
      };
    },
    91495: (t, e, n) => {
      var r = n(42582),
        o = 1 / 0;
      t.exports = function (t) {
        return t
          ? (t = r(t)) === o || t === -1 / 0
            ? 17976931348623157e292 * (t < 0 ? -1 : 1)
            : t === t
              ? t
              : 0
          : 0 === t
            ? t
            : 0;
      };
    },
    39753: (t, e, n) => {
      var r = n(91495);
      t.exports = function (t) {
        var e = r(t),
          n = e % 1;
        return e === e ? (n ? e - n : e) : 0;
      };
    },
    42582: (t, e, n) => {
      var r = n(20821),
        o = n(8092),
        a = n(70152),
        i = /^[-+]0x[0-9a-f]+$/i,
        c = /^0b[01]+$/i,
        l = /^0o[0-7]+$/i,
        u = parseInt;
      t.exports = function (t) {
        if ("number" == typeof t) return t;
        if (a(t)) return NaN;
        if (o(t)) {
          var e = "function" == typeof t.valueOf ? t.valueOf() : t;
          t = o(e) ? e + "" : e;
        }
        if ("string" != typeof t) return 0 === t ? t : +t;
        t = r(t);
        var n = c.test(t);
        return n || l.test(t) ? u(t.slice(2), n ? 2 : 8) : i.test(t) ? NaN : +t;
      };
    },
    63518: (t, e, n) => {
      var r = n(2446);
      t.exports = function (t) {
        return null == t ? "" : r(t);
      };
    },
    72064: (t, e, n) => {
      var r = n(39602);
      t.exports = function (t) {
        return t && t.length ? r(t) : [];
      };
    },
    66339: (t, e, n) => {
      var r = n(56025),
        o = n(39602);
      t.exports = function (t, e) {
        return t && t.length ? o(t, r(e, 2)) : [];
      };
    },
    30804: (t, e, n) => {
      var r = n(63518),
        o = 0;
      t.exports = function (t) {
        var e = ++o;
        return r(t) + e;
      };
    },
    92063: (t, e, n) => {
      var r = n(28019),
        o = n(12742);
      t.exports = function (t) {
        return null == t ? [] : r(t, o(t));
      };
    },
    41761: (t, e, n) => {
      var r = n(21468),
        o = n(58794),
        a = n(56279),
        i = o(function (t, e) {
          return a(t) ? r(t, e) : [];
        });
      t.exports = i;
    },
    50077: (t) => {
      var e = "undefined" !== typeof Element,
        n = "function" === typeof Map,
        r = "function" === typeof Set,
        o = "function" === typeof ArrayBuffer && !!ArrayBuffer.isView;
      function a(t, i) {
        if (t === i) return !0;
        if (t && i && "object" == typeof t && "object" == typeof i) {
          if (t.constructor !== i.constructor) return !1;
          var c, l, u, s;
          if (Array.isArray(t)) {
            if ((c = t.length) != i.length) return !1;
            for (l = c; 0 !== l--; ) if (!a(t[l], i[l])) return !1;
            return !0;
          }
          if (n && t instanceof Map && i instanceof Map) {
            if (t.size !== i.size) return !1;
            for (s = t.entries(); !(l = s.next()).done; )
              if (!i.has(l.value[0])) return !1;
            for (s = t.entries(); !(l = s.next()).done; )
              if (!a(l.value[1], i.get(l.value[0]))) return !1;
            return !0;
          }
          if (r && t instanceof Set && i instanceof Set) {
            if (t.size !== i.size) return !1;
            for (s = t.entries(); !(l = s.next()).done; )
              if (!i.has(l.value[0])) return !1;
            return !0;
          }
          if (o && ArrayBuffer.isView(t) && ArrayBuffer.isView(i)) {
            if ((c = t.length) != i.length) return !1;
            for (l = c; 0 !== l--; ) if (t[l] !== i[l]) return !1;
            return !0;
          }
          if (t.constructor === RegExp)
            return t.source === i.source && t.flags === i.flags;
          if (
            t.valueOf !== Object.prototype.valueOf &&
            "function" === typeof t.valueOf &&
            "function" === typeof i.valueOf
          )
            return t.valueOf() === i.valueOf();
          if (
            t.toString !== Object.prototype.toString &&
            "function" === typeof t.toString &&
            "function" === typeof i.toString
          )
            return t.toString() === i.toString();
          if ((c = (u = Object.keys(t)).length) !== Object.keys(i).length)
            return !1;
          for (l = c; 0 !== l--; )
            if (!Object.prototype.hasOwnProperty.call(i, u[l])) return !1;
          if (e && t instanceof Element) return !1;
          for (l = c; 0 !== l--; )
            if (
              (("_owner" !== u[l] && "__v" !== u[l] && "__o" !== u[l]) ||
                !t.$$typeof) &&
              !a(t[u[l]], i[u[l]])
            )
              return !1;
          return !0;
        }
        return t !== t && i !== i;
      }
      t.exports = function (t, e) {
        try {
          return a(t, e);
        } catch (n) {
          if ((n.message || "").match(/stack|recursion/i))
            return (
              console.warn("react-fast-compare cannot handle circular refs"), !1
            );
          throw n;
        }
      };
    },
    11372: (t, e) => {
      "use strict";
      var n = "function" === typeof Symbol && Symbol.for,
        r = n ? Symbol.for("react.element") : 60103,
        o = n ? Symbol.for("react.portal") : 60106,
        a = n ? Symbol.for("react.fragment") : 60107,
        i = n ? Symbol.for("react.strict_mode") : 60108,
        c = n ? Symbol.for("react.profiler") : 60114,
        l = n ? Symbol.for("react.provider") : 60109,
        u = n ? Symbol.for("react.context") : 60110,
        s = n ? Symbol.for("react.async_mode") : 60111,
        f = n ? Symbol.for("react.concurrent_mode") : 60111,
        p = n ? Symbol.for("react.forward_ref") : 60112,
        d = n ? Symbol.for("react.suspense") : 60113,
        h = n ? Symbol.for("react.suspense_list") : 60120,
        v = n ? Symbol.for("react.memo") : 60115,
        y = n ? Symbol.for("react.lazy") : 60116,
        m = n ? Symbol.for("react.block") : 60121,
        g = n ? Symbol.for("react.fundamental") : 60117,
        b = n ? Symbol.for("react.responder") : 60118,
        x = n ? Symbol.for("react.scope") : 60119;
      function O(t) {
        if ("object" === typeof t && null !== t) {
          var e = t.$$typeof;
          switch (e) {
            case r:
              switch ((t = t.type)) {
                case s:
                case f:
                case a:
                case c:
                case i:
                case d:
                  return t;
                default:
                  switch ((t = t && t.$$typeof)) {
                    case u:
                    case p:
                    case y:
                    case v:
                    case l:
                      return t;
                    default:
                      return e;
                  }
              }
            case o:
              return e;
          }
        }
      }
      function w(t) {
        return O(t) === f;
      }
      (e.AsyncMode = s),
        (e.ConcurrentMode = f),
        (e.ContextConsumer = u),
        (e.ContextProvider = l),
        (e.Element = r),
        (e.ForwardRef = p),
        (e.Fragment = a),
        (e.Lazy = y),
        (e.Memo = v),
        (e.Portal = o),
        (e.Profiler = c),
        (e.StrictMode = i),
        (e.Suspense = d),
        (e.isAsyncMode = function (t) {
          return w(t) || O(t) === s;
        }),
        (e.isConcurrentMode = w),
        (e.isContextConsumer = function (t) {
          return O(t) === u;
        }),
        (e.isContextProvider = function (t) {
          return O(t) === l;
        }),
        (e.isElement = function (t) {
          return "object" === typeof t && null !== t && t.$$typeof === r;
        }),
        (e.isForwardRef = function (t) {
          return O(t) === p;
        }),
        (e.isFragment = function (t) {
          return O(t) === a;
        }),
        (e.isLazy = function (t) {
          return O(t) === y;
        }),
        (e.isMemo = function (t) {
          return O(t) === v;
        }),
        (e.isPortal = function (t) {
          return O(t) === o;
        }),
        (e.isProfiler = function (t) {
          return O(t) === c;
        }),
        (e.isStrictMode = function (t) {
          return O(t) === i;
        }),
        (e.isSuspense = function (t) {
          return O(t) === d;
        }),
        (e.isValidElementType = function (t) {
          return (
            "string" === typeof t ||
            "function" === typeof t ||
            t === a ||
            t === f ||
            t === c ||
            t === i ||
            t === d ||
            t === h ||
            ("object" === typeof t &&
              null !== t &&
              (t.$$typeof === y ||
                t.$$typeof === v ||
                t.$$typeof === l ||
                t.$$typeof === u ||
                t.$$typeof === p ||
                t.$$typeof === g ||
                t.$$typeof === b ||
                t.$$typeof === x ||
                t.$$typeof === m))
          );
        }),
        (e.typeOf = O);
    },
    57441: (t, e, n) => {
      "use strict";
      t.exports = n(11372);
    },
    60344: (t, e, n) => {
      "use strict";
      n.d(e, { E: () => tt });
      var r = n(66364),
        o = n.n(r),
        a = n(15687),
        i = n.n(a),
        c = n(52007),
        l = n.n(c),
        u = n(72791),
        s = n(4463),
        f = n(62795),
        p = n(97409),
        d = n(46577),
        h = n(42745),
        v = n(53841),
        y = n(83485),
        m = n(58853),
        g = n(17792),
        b = n(86225),
        x = n(66933),
        O = n.n(x),
        w = n(20933),
        C = n(8091);
      function S(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return A(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return A(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return A(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function A(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function j(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      var k = { top: -1, left: -1, right: 1, bottom: 1 },
        P = function (t) {
          return null !== t && void 0 !== t;
        },
        E = function (t, e) {
          var n = t.style || {};
          e = e || {};
          return {
            parent: O()(n.parent, e.parent, { height: "100%", width: "100%" }),
            axis: O()({}, n.axis, e.axis),
            axisLabel: O()({}, n.axisLabel, e.axisLabel),
            grid: O()({}, n.grid, e.grid),
            ticks: O()({}, n.ticks, e.ticks),
            tickLabels: O()({}, n.tickLabels, e.tickLabels),
          };
        },
        M = function (t, e, n) {
          var r = t.position,
            o = t.transform;
          return {
            x1: o.x,
            y1: o.y,
            x2: o.x + r.x2,
            y2: o.y + r.y2,
            style: e,
            datum: n,
          };
        },
        T = function (t, e, n, r, o) {
          var a = t.position,
            i = t.transform;
          return {
            style: e,
            x: i.x + a.x,
            y: i.y + a.y,
            verticalAnchor: n.verticalAnchor,
            textAnchor: n.textAnchor,
            angle: e.angle,
            text: o,
            datum: r,
          };
        },
        _ = function (t, e, n) {
          var r = t.edge,
            o = t.transform;
          return {
            x1: o.x,
            y1: o.y,
            x2: r.x + o.x,
            y2: r.y + o.y,
            style: e,
            datum: n,
          };
        },
        L = function (t, e, n) {
          var r = e || "positive";
          return n
            ? {
                positive: { x: "left", y: "bottom" },
                negative: { x: "right", y: "top" },
              }[r][t]
            : {
                positive: { x: "bottom", y: "left" },
                negative: { x: "top", y: "right" },
              }[r][t];
        },
        D = function (t, e) {
          return t instanceof Date && e instanceof Date
            ? t.getTime() === e.getTime()
            : t === e;
        },
        I = function (t, e, n) {
          var r = e.orientation,
            o = e.axis,
            a = s.w5(t, o);
          return {
            top: { x: 0, y: void 0 !== a ? a : n.y },
            bottom: { x: 0, y: void 0 !== a ? a : t.height - n.y },
            left: { x: void 0 !== a ? a : n.x, y: 0 },
            right: { x: void 0 !== a ? a : t.width - n.x, y: 0 },
          }[r];
        },
        R = function (t, e, n) {
          var r = t.tickStyle,
            o = t.labelStyle,
            a = r.size || 0,
            i = a + (r.padding || 0) + (o.padding || 0),
            c = k[e];
          return {
            x: n ? c * i : 0,
            x2: n ? c * a : 0,
            y: n ? 0 : c * i,
            y2: n ? 0 : c * a,
          };
        },
        N = function (t, e, n) {
          return { x: n ? e.x : t + e.x, y: n ? t + e.y : e.y };
        },
        W = function (t, e) {
          var n = e.orientation,
            r = e.padding,
            o = e.isVertical,
            a = -k[n];
          return {
            x: o ? a * (t.width - (r.left + r.right)) : 0,
            y: o ? 0 : a * (t.height - (r.top + r.bottom)),
          };
        },
        F = function (t, e) {
          var n = t.padding,
            r = t.orientation,
            o = t.crossAxis,
            a = "right" === r ? n.right : n.left,
            i = "top" === r ? n.top : n.bottom;
          return { x: o ? e.x - a : 0, y: o ? e.y - i : 0 };
        },
        z = function (t, e) {
          var n;
          return (
            (n =
              e.domain.x && e.domain.y
                ? t.horizontal
                  ? (function (t, e) {
                      var n = e.scale,
                        r = e.origin,
                        o = e.orientation,
                        a = e.orientations,
                        i = e.domain,
                        c = e.padding,
                        l = c.top,
                        u = c.bottom,
                        s = c.left,
                        f = c.right,
                        p = "bottom" === o || "top" === o ? o : a.x,
                        d = "left" === o || "right" === o ? o : a.y,
                        h = {
                          x: "bottom" === p ? u : l,
                          y: "left" === d ? s : f,
                        },
                        v = "left" === d ? 0 : t.width,
                        y = "bottom" === p ? t.height : 0,
                        m = D(r.x, i.x[0]) || D(r.x, i.x[1]) ? 0 : n.x(r.x),
                        g = D(r.y, i.y[0]) || D(r.y, i.y[1]) ? 0 : n.y(r.y),
                        b = m ? Math.abs(y - m) : h.x,
                        x = g ? Math.abs(v - g) : h.y;
                      return {
                        x: P(t.offsetX) ? t.offsetX : x,
                        y: P(t.offsetY) ? t.offsetY : b,
                      };
                    })(t, e)
                  : (function (t, e) {
                      var n = e.scale,
                        r = e.origin,
                        o = e.orientation,
                        a = e.orientations,
                        i = e.domain,
                        c = e.padding,
                        l = c.top,
                        u = c.bottom,
                        s = c.left,
                        f = c.right,
                        p = "bottom" === o || "top" === o ? o : a.x,
                        d = "left" === o || "right" === o ? o : a.y,
                        h = {
                          x: "left" === d ? s : f,
                          y: "bottom" === p ? u : l,
                        },
                        v = "left" === d ? 0 : t.width,
                        y = "bottom" === p ? t.height : 0,
                        m = D(r.x, i.x[0]) || D(r.x, i.x[1]) ? 0 : n.x(r.x),
                        g = D(r.y, i.y[0]) || D(r.y, i.y[1]) ? 0 : n.y(r.y),
                        b = m ? Math.abs(v - m) : h.x,
                        x = g ? Math.abs(y - g) : h.y;
                      return {
                        x: P(t.offsetX) ? t.offsetX : b,
                        y: P(t.offsetY) ? t.offsetY : x,
                      };
                    })(t, e)
                : (function (t, e) {
                    var n = e.style,
                      r = e.scale,
                      o = e.orientation,
                      a = e.padding,
                      c = e.axis,
                      l = e.ticks,
                      u = e.stringTicks,
                      s = e.isVertical,
                      f = e.labelPadding,
                      p = t.polar,
                      d = t.horizontal,
                      h = {
                        scale: j({}, c, r),
                        polar: p,
                        horizontal: d,
                        ticks: l,
                        stringTicks: u,
                      },
                      v = "right" === o ? a.right : a.left,
                      y = "top" === o ? a.top : a.bottom,
                      m =
                        null !== t.offsetX && void 0 !== t.offsetX
                          ? t.offsetX
                          : v,
                      g =
                        null !== t.offsetY && void 0 !== t.offsetY
                          ? t.offsetY
                          : y,
                      b = n.axisLabel.fontSize || 14,
                      x = l.map(function (e, r) {
                        var o = u ? t.tickValues[e - 1] : e;
                        return (
                          C.F3(n.ticks, i()({}, h, { tick: o, index: r }))
                            .size || 0
                        );
                      }),
                      O = b + 2 * Math.max.apply(Math, S(x)) + f,
                      w = 1.2 * b;
                    return {
                      x: null !== m && void 0 !== m ? m : s ? O : w,
                      y: null !== g && void 0 !== g ? g : s ? w : O,
                    };
                  })(t, e)),
            {
              globalTransform: I(t, e, n),
              gridOffset: F(e, n),
              gridEdge: W(t, e),
            }
          );
        },
        U = function (t) {
          var e = (function (t) {
              var e = t.theme,
                n = t.dependentAxis,
                r = e && e.axis && e.axis.style,
                o = n ? "dependentAxis" : "independentAxis",
                a = e && e[o] && e[o].style;
              return r && a
                ? [
                    "axis",
                    "axisLabel",
                    "grid",
                    "parent",
                    "tickLabels",
                    "ticks",
                  ].reduce(function (t, e) {
                    return (t[e] = O()({}, a[e], r[e])), t;
                  }, {})
                : a || r;
            })(t),
            n = E(t, e),
            r = C.tQ(t),
            o = (function (t, e) {
              var n = e.axisLabel || {};
              if (void 0 !== n.padding && null !== n.padding) return n.padding;
              var r = s.cp(t),
                o = n.fontSize || 14;
              return t.label ? o * (r ? 2.3 : 1.6) : 0;
            })(t, n),
            a = s.kM(t) ? t.tickValues : void 0,
            i = s.dd(t),
            c = s.ge(t),
            l = (function (t) {
              var e = s.dd(t),
                n = (function (t, e) {
                  var n = t.orientation,
                    r = t.horizontal;
                  return n
                    ? { top: "x", bottom: "x", left: "y", right: "y" }[n]
                    : r
                      ? "x" === e
                        ? "y"
                        : "x"
                      : e;
                })(t, e),
                r = w.q8(t, e),
                o = (t.domain && t.domain[e]) || s.ge(t) || r.domain();
              return r.range(C.rx(t, n)), r.domain(o), r;
            })(t),
            u = "x" === i ? c : void 0,
            f = "y" === i ? c : void 0,
            p = "x" === i ? l : void 0,
            d = "y" === i ? l : void 0,
            h = !(!1 === t.crossAxis || !0 === t.standalone),
            v = s.fj(t, l, h),
            y = s.Js(t, l),
            m = { x: C.rx(t, "x"), y: C.rx(t, "y") },
            g = {
              x: t.domain && t.domain.x ? t.domain.x : u,
              y: t.domain && t.domain.y ? t.domain.y : f,
            },
            b = {
              x:
                t.domain && t.domain.x
                  ? w
                      .q8(t, "x")
                      .domain(t.domain.x)
                      .range(t.horizontal ? m.y : m.x)
                  : p,
              y:
                t.domain && t.domain.y
                  ? w
                      .q8(t, "y")
                      .domain(t.domain.y)
                      .range(t.horizontal ? m.x : m.y)
                  : d,
            },
            x = g.x && g.y ? s.P$(g) : void 0,
            S = x ? { x: s.eE(x.x, g.x), y: s.eE(x.y, g.y) } : void 0,
            A = S
              ? { x: L("x", S.y, t.horizontal), y: L("y", S.x, t.horizontal) }
              : void 0,
            j = A
              ? t.orientation || A[i]
              : (function (t) {
                  if (t.orientation) return t.orientation;
                  var e = {
                    dependent: t.horizontal ? "bottom" : "left",
                    independent: t.horizontal ? "left" : "bottom",
                  };
                  return t.dependentAxis ? e.dependent : e.independent;
                })(t),
            k = s.cp(Object.assign({}, t, { orientation: j })),
            P = (function (t, e) {
              var n = {
                top: "end",
                left: "end",
                right: "start",
                bottom: "start",
              }[t];
              return {
                textAnchor: e ? n : "middle",
                verticalAnchor: e ? "middle" : n,
              };
            })(j, k);
          return {
            anchors: P,
            axis: i,
            crossAxis: h,
            domain: g,
            isVertical: k,
            labelPadding: o,
            orientation: j,
            orientations: A,
            origin: x,
            padding: r,
            scale: b,
            stringTicks: a,
            style: n,
            tickFormat: y,
            ticks: v,
          };
        },
        B = function (t, e) {
          t = s.TY(t, e);
          var n = U(t),
            r = n.axis,
            o = n.style,
            a = n.orientation,
            c = n.isVertical,
            l = n.scale,
            u = n.ticks,
            f = n.tickFormat,
            p = n.anchors,
            d = n.domain,
            h = n.stringTicks,
            v = "x" === r ? "y" : "x",
            y = t,
            m = y.width,
            g = y.height,
            b = y.standalone,
            x = y.theme,
            O = y.polar,
            w = y.padding,
            S = y.horizontal,
            A = z(t, n),
            P = A.globalTransform,
            E = A.gridOffset,
            L = A.gridEdge,
            D = {
              scale: j({}, r, l[r]),
              polar: O,
              horizontal: S,
              ticks: u,
              stringTicks: h,
            },
            I = (function (t, e, n) {
              var r = e.style,
                o = e.padding,
                a = e.isVertical,
                i = t.width,
                c = t.height;
              return {
                style: r.axis,
                x1: a ? n.x : o.left + n.x,
                x2: a ? n.x : i - o.right + n.x,
                y1: a ? o.top + n.y : n.y,
                y2: a ? c - o.bottom + n.y : n.y,
              };
            })(t, n, P),
            W = (function (t, e, n) {
              var r = e.style,
                o = e.orientation,
                a = e.padding,
                i = e.labelPadding,
                c = e.isVertical,
                l = k[o],
                u = a.left + a.right,
                s = a.top + a.bottom,
                f = l < 0 ? "end" : "start",
                p = r.axisLabel,
                d = c ? -90 : 0;
              return {
                x: c ? n.x + l * i : (t.width - u) / 2 + a.left + n.x,
                y: c ? (t.height - s) / 2 + a.top + n.y : l * i + n.y,
                verticalAnchor: p.verticalAnchor || f,
                textAnchor: p.textAnchor || "middle",
                angle: void 0 === p.angle ? d : p.angle,
                style: p,
                text: t.label,
              };
            })(t, n, P),
            F = {
              parent: i()(
                {
                  style: o.parent,
                  ticks: u,
                  standalone: b,
                  theme: x,
                  width: m,
                  height: g,
                  padding: w,
                  domain: d,
                },
                D,
              ),
            },
            B = {
              dimension: v,
              range: j({}, v, C.rx(t, v)),
              scale: t.scale && t.scale[v] ? j({}, v, t.scale[v]) : void 0,
            };
          return u.reduce(function (t, e, n) {
            var s,
              d,
              v,
              y = h ? h[n] : e,
              m = f(e, n, u),
              g = (function (t, e) {
                return {
                  tickStyle: C.F3(t.ticks, e),
                  labelStyle: C.F3(t.tickLabels, e),
                  gridStyle: C.F3(t.grid, e),
                };
              })(o, i()({}, D, { tick: y, tickValue: e, index: n, text: m })),
              b = {
                position: R(g, a, c),
                transform: N(
                  null === (s = l[r]) || void 0 === s ? void 0 : s.call(l, e),
                  P,
                  c,
                ),
              },
              x = {
                edge: L,
                transform: {
                  x: c
                    ? -E.x + P.x
                    : (null === (d = l[r]) || void 0 === d
                        ? void 0
                        : d.call(l, e)) + P.x,
                  y: c
                    ? (null === (v = l[r]) || void 0 === v
                        ? void 0
                        : v.call(l, e)) + P.y
                    : E.y + P.y,
                },
              };
            return (
              (t[n] = {
                axis: i()({ dimension: r }, D, I),
                axisLabel: i()({}, D, W),
                ticks: i()({}, D, M(b, g.tickStyle, e)),
                tickLabels: i()({}, D, T(b, g.labelStyle, p, e, m)),
                grid: i()({}, D, B, _(x, g.gridStyle, e)),
              }),
              t
            );
          }, F);
        };
      function q(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function H(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? q(Object(n), !0).forEach(function (e) {
                V(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : q(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function V(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      function $(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return Y(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return Y(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return Y(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function Y(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function Z(t, e) {
        for (var n = 0; n < e.length; n++) {
          var r = e[n];
          (r.enumerable = r.enumerable || !1),
            (r.configurable = !0),
            "value" in r && (r.writable = !0),
            Object.defineProperty(t, r.key, r);
        }
      }
      function K(t, e) {
        return (
          (K = Object.setPrototypeOf
            ? Object.setPrototypeOf.bind()
            : function (t, e) {
                return (t.__proto__ = e), t;
              }),
          K(t, e)
        );
      }
      function G(t) {
        var e = (function () {
          if ("undefined" === typeof Reflect || !Reflect.construct) return !1;
          if (Reflect.construct.sham) return !1;
          if ("function" === typeof Proxy) return !0;
          try {
            return (
              Boolean.prototype.valueOf.call(
                Reflect.construct(Boolean, [], function () {}),
              ),
              !0
            );
          } catch (t) {
            return !1;
          }
        })();
        return function () {
          var n,
            r = X(t);
          if (e) {
            var o = X(this).constructor;
            n = Reflect.construct(r, arguments, o);
          } else n = r.apply(this, arguments);
          return (function (t, e) {
            if (e && ("object" === typeof e || "function" === typeof e))
              return e;
            if (void 0 !== e)
              throw new TypeError(
                "Derived constructors may only return object or undefined",
              );
            return (function (t) {
              if (void 0 === t)
                throw new ReferenceError(
                  "this hasn't been initialised - super() hasn't been called",
                );
              return t;
            })(t);
          })(this, n);
        };
      }
      function X(t) {
        return (
          (X = Object.setPrototypeOf
            ? Object.getPrototypeOf.bind()
            : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t);
              }),
          X(t)
        );
      }
      var Q = { width: 450, height: 300, padding: 50 },
        J = (function (t) {
          !(function (t, e) {
            if ("function" !== typeof e && null !== e)
              throw new TypeError(
                "Super expression must either be null or a function",
              );
            (t.prototype = Object.create(e && e.prototype, {
              constructor: { value: t, writable: !0, configurable: !0 },
            })),
              Object.defineProperty(t, "prototype", { writable: !1 }),
              e && K(t, e);
          })(c, t);
          var e,
            n,
            r,
            a = G(c);
          function c() {
            return (
              (function (t, e) {
                if (!(t instanceof e))
                  throw new TypeError("Cannot call a class as a function");
              })(this, c),
              a.apply(this, arguments)
            );
          }
          return (
            (e = c),
            (n = [
              {
                key: "renderLine",
                value: function (t) {
                  var e = t.axisComponent,
                    n = this.getComponentProps(e, "axis", 0);
                  return u.cloneElement(e, n);
                },
              },
              {
                key: "renderLabel",
                value: function (t) {
                  var e = t.axisLabelComponent;
                  if (!t.label) return null;
                  var n = this.getComponentProps(e, "axisLabel", 0);
                  return u.cloneElement(e, n);
                },
              },
              {
                key: "renderGridAndTicks",
                value: function (t) {
                  var e = this,
                    n = t.tickComponent,
                    r = t.tickLabelComponent,
                    a = t.gridComponent,
                    i = t.name,
                    c = function (t) {
                      var e = t.style,
                        n = void 0 === e ? {} : e,
                        r = t.events,
                        a = void 0 === r ? {} : r;
                      return (
                        ("transparent" !== n.stroke &&
                          "none" !== n.stroke &&
                          0 !== n.strokeWidth) ||
                        !o()(a)
                      );
                    };
                  return this.dataKeys.map(function (o, l) {
                    var s = e.getComponentProps(n, "ticks", l),
                      f = u.cloneElement(n, s),
                      p = c(f.props) ? f : void 0,
                      d = e.getComponentProps(a, "grid", l),
                      h = u.cloneElement(a, d),
                      v = c(h.props) ? h : void 0,
                      y = e.getComponentProps(r, "tickLabels", l),
                      m = [v, p, u.cloneElement(r, y)].filter(Boolean);
                    return u.cloneElement(
                      t.groupComponent,
                      { key: "".concat(i, "-tick-group-").concat(o) },
                      m,
                    );
                  });
                },
              },
              {
                key: "fixLabelOverlap",
                value: function (t, e) {
                  var n = s.cp(e),
                    r = n ? e.height : e.width,
                    o = function (t) {
                      return t.type && "label" === t.type.role;
                    },
                    a = t
                      .map(function (t) {
                        return t.props.children;
                      })
                      .reduce(function (t, e) {
                        return t.concat(e);
                      }, [])
                      .filter(o)
                      .map(function (t) {
                        return t.props;
                      }),
                    c = a.reduce(function (t, e) {
                      var r = (function (t) {
                          return "object" === typeof t
                            ? i()(
                                {},
                                { top: 0, right: 0, bottom: 0, left: 0 },
                                t,
                              )
                            : { top: t, right: t, bottom: t, left: t };
                        })(e.style.padding),
                        o = f.Z9(e.text, {
                          angle: e.angle,
                          fontSize: e.style.fontSize,
                          letterSpacing: e.style.letterSpacing,
                          fontFamily: e.style.fontFamily,
                        });
                      return (
                        t +
                        (n
                          ? o.height + r.top + r.bottom
                          : o.width + r.right + r.left)
                      );
                    }, 0),
                    l = Math.floor((r * t.length) / c),
                    u = Math.ceil(t.length / l) || 1,
                    p = function (t) {
                      return t.props.children.filter(o).reduce(function (t, e) {
                        return (n ? e.props.y : e.props.x) || 0;
                      }, 0);
                    };
                  return t
                    .sort(function (t, e) {
                      return n ? p(e) - p(t) : p(t) - p(e);
                    })
                    .filter(function (t, e) {
                      return e % u === 0;
                    });
                },
              },
              {
                key: "shouldAnimate",
                value: function () {
                  return !!this.props.animate;
                },
              },
              {
                key: "render",
                value: function () {
                  var t = tt.animationWhitelist,
                    e = s.TY(this.props, Q),
                    n = p.I(this.props);
                  if (this.shouldAnimate()) return this.animateComponent(e, t);
                  var r = this.renderGridAndTicks(e),
                    o = e.fixLabelOverlap ? this.fixLabelOverlap(r, e) : r,
                    a = [this.renderLine(e), this.renderLabel(e)].concat($(o)),
                    i = u.cloneElement(e.containerComponent, n);
                  return e.standalone
                    ? this.renderContainer(i, a)
                    : u.cloneElement(e.groupComponent, n, a);
                },
              },
            ]) && Z(e.prototype, n),
            r && Z(e, r),
            Object.defineProperty(e, "prototype", { writable: !1 }),
            c
          );
        })(u.Component);
      (J.animationWhitelist = [
        "style",
        "domain",
        "range",
        "tickCount",
        "tickValues",
        "offsetX",
        "offsetY",
        "padding",
        "width",
        "height",
      ]),
        (J.displayName = "VictoryAxis"),
        (J.role = "axis"),
        (J.defaultTransitions = {
          onExit: { duration: 500 },
          onEnter: { duration: 500 },
        }),
        (J.propTypes = H(
          H({}, d.l.baseProps),
          {},
          {
            axisComponent: l().element,
            axisLabelComponent: l().element,
            axisValue: l().oneOfType([l().number, l().string, l().object]),
            categories: l().oneOfType([
              l().arrayOf(l().string),
              l().shape({
                x: l().arrayOf(l().string),
                y: l().arrayOf(l().string),
              }),
            ]),
            crossAxis: l().bool,
            dependentAxis: l().bool,
            events: l().arrayOf(
              l().shape({
                target: l().oneOf([
                  "axis",
                  "axisLabel",
                  "grid",
                  "ticks",
                  "tickLabels",
                ]),
                eventKey: l().oneOfType([
                  l().array,
                  h.BO([h._L, h.A7]),
                  l().string,
                ]),
                eventHandlers: l().object,
              }),
            ),
            fixLabelOverlap: l().bool,
            gridComponent: l().element,
            groupComponent: l().element,
            invertAxis: l().bool,
            label: l().any,
            offsetX: l().number,
            offsetY: l().number,
            orientation: l().oneOf(["top", "bottom", "left", "right"]),
            origin: l().shape({ x: l().number, y: l().number }),
            stringMap: l().object,
            style: l().shape({
              parent: l().object,
              axis: l().object,
              axisLabel: l().object,
              grid: l().object,
              ticks: l().object,
              tickLabels: l().object,
            }),
            tickComponent: l().element,
            tickCount: h.BO([h._L, h.KO]),
            tickFormat: l().oneOfType([l().func, h.xx]),
            tickLabelComponent: l().element,
            tickValues: h.xx,
          },
        )),
        (J.defaultProps = {
          axisComponent: u.createElement(v.c, null),
          axisLabelComponent: u.createElement(y.X, null),
          tickLabelComponent: u.createElement(y.X, null),
          tickComponent: u.createElement(v.c, null),
          gridComponent: u.createElement(v.c, null),
          standalone: !0,
          theme: m.J.grayscale,
          containerComponent: u.createElement(g._, null),
          groupComponent: u.createElement("g", { role: "presentation" }),
          fixLabelOverlap: !1,
        }),
        (J.getDomain = s.ge),
        (J.getAxis = s.dd),
        (J.getStyles = function (t) {
          return E(t);
        }),
        (J.getBaseProps = function (t) {
          return B(t, Q);
        }),
        (J.expectedComponents = [
          "axisComponent",
          "axisLabelComponent",
          "groupComponent",
          "containerComponent",
          "tickComponent",
          "tickLabelComponent",
          "gridComponent",
        ]);
      var tt = (0, b.o)(J, {
        components: [
          { name: "axis", index: 0 },
          { name: "axisLabel", index: 0 },
          { name: "grid" },
          { name: "parent", index: "parent" },
          { name: "ticks" },
          { name: "tickLabels" },
        ],
      });
    },
    17792: (t, e, n) => {
      "use strict";
      n.d(e, { _: () => R });
      var r = n(74786),
        o = n.n(r),
        a = n(8092),
        i = n.n(a),
        c = n(30804),
        l = n.n(c),
        u = n(66933),
        s = n.n(u),
        f = n(15687),
        p = n.n(f),
        d = n(72791),
        h = n(52007),
        v = n.n(h),
        y = n(42745),
        m = n(12742),
        g = n.n(m);
      function b(t, e) {
        for (var n = 0; n < e.length; n++) {
          var r = e[n];
          (r.enumerable = r.enumerable || !1),
            (r.configurable = !0),
            "value" in r && (r.writable = !0),
            Object.defineProperty(t, r.key, r);
        }
      }
      function x(t, e) {
        return (
          (x = Object.setPrototypeOf
            ? Object.setPrototypeOf.bind()
            : function (t, e) {
                return (t.__proto__ = e), t;
              }),
          x(t, e)
        );
      }
      function O(t) {
        var e = (function () {
          if ("undefined" === typeof Reflect || !Reflect.construct) return !1;
          if (Reflect.construct.sham) return !1;
          if ("function" === typeof Proxy) return !0;
          try {
            return (
              Boolean.prototype.valueOf.call(
                Reflect.construct(Boolean, [], function () {}),
              ),
              !0
            );
          } catch (t) {
            return !1;
          }
        })();
        return function () {
          var n,
            r = w(t);
          if (e) {
            var o = w(this).constructor;
            n = Reflect.construct(r, arguments, o);
          } else n = r.apply(this, arguments);
          return (function (t, e) {
            if (e && ("object" === typeof e || "function" === typeof e))
              return e;
            if (void 0 !== e)
              throw new TypeError(
                "Derived constructors may only return object or undefined",
              );
            return (function (t) {
              if (void 0 === t)
                throw new ReferenceError(
                  "this hasn't been initialised - super() hasn't been called",
                );
              return t;
            })(t);
          })(this, n);
        };
      }
      function w(t) {
        return (
          (w = Object.setPrototypeOf
            ? Object.getPrototypeOf.bind()
            : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t);
              }),
          w(t)
        );
      }
      var C = (function (t) {
        !(function (t, e) {
          if ("function" !== typeof e && null !== e)
            throw new TypeError(
              "Super expression must either be null or a function",
            );
          (t.prototype = Object.create(e && e.prototype, {
            constructor: { value: t, writable: !0, configurable: !0 },
          })),
            Object.defineProperty(t, "prototype", { writable: !1 }),
            e && x(t, e);
        })(a, t);
        var e,
          n,
          r,
          o = O(a);
        function a(t) {
          var e;
          return (
            (function (t, e) {
              if (!(t instanceof e))
                throw new TypeError("Cannot call a class as a function");
            })(this, a),
            ((e = o.call(this, t)).map = void 0),
            (e.index = void 0),
            (e.portalRegister = function () {
              return ++e.index;
            }),
            (e.portalUpdate = function (t, n) {
              (e.map[t] = n), e.forceUpdate();
            }),
            (e.portalDeregister = function (t) {
              delete e.map[t], e.forceUpdate();
            }),
            (e.map = {}),
            (e.index = 1),
            e
          );
        }
        return (
          (e = a),
          (n = [
            {
              key: "getChildren",
              value: function () {
                var t = this;
                return g()(this.map).map(function (e) {
                  var n = t.map[e];
                  return n ? d.cloneElement(n, { key: e }) : n;
                });
              },
            },
            {
              key: "render",
              value: function () {
                return d.createElement("svg", this.props, this.getChildren());
              },
            },
          ]) && b(e.prototype, n),
          r && b(e, r),
          Object.defineProperty(e, "prototype", { writable: !1 }),
          a
        );
      })(d.Component);
      (C.displayName = "Portal"),
        (C.propTypes = {
          className: v().string,
          height: y.A7,
          style: v().object,
          viewBox: v().string,
          width: y.A7,
        });
      var S = n(64606),
        A = n(91002),
        j = n(8091),
        k = n(97409);
      function P() {
        return (
          (P = Object.assign
            ? Object.assign.bind()
            : function (t) {
                for (var e = 1; e < arguments.length; e++) {
                  var n = arguments[e];
                  for (var r in n)
                    Object.prototype.hasOwnProperty.call(n, r) && (t[r] = n[r]);
                }
                return t;
              }),
          P.apply(this, arguments)
        );
      }
      function E(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function M(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? E(Object(n), !0).forEach(function (e) {
                T(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : E(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function T(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      function _(t, e) {
        for (var n = 0; n < e.length; n++) {
          var r = e[n];
          (r.enumerable = r.enumerable || !1),
            (r.configurable = !0),
            "value" in r && (r.writable = !0),
            Object.defineProperty(t, r.key, r);
        }
      }
      function L(t, e) {
        return (
          (L = Object.setPrototypeOf
            ? Object.setPrototypeOf.bind()
            : function (t, e) {
                return (t.__proto__ = e), t;
              }),
          L(t, e)
        );
      }
      function D(t) {
        var e = (function () {
          if ("undefined" === typeof Reflect || !Reflect.construct) return !1;
          if (Reflect.construct.sham) return !1;
          if ("function" === typeof Proxy) return !0;
          try {
            return (
              Boolean.prototype.valueOf.call(
                Reflect.construct(Boolean, [], function () {}),
              ),
              !0
            );
          } catch (t) {
            return !1;
          }
        })();
        return function () {
          var n,
            r = I(t);
          if (e) {
            var o = I(this).constructor;
            n = Reflect.construct(r, arguments, o);
          } else n = r.apply(this, arguments);
          return (function (t, e) {
            if (e && ("object" === typeof e || "function" === typeof e))
              return e;
            if (void 0 !== e)
              throw new TypeError(
                "Derived constructors may only return object or undefined",
              );
            return (function (t) {
              if (void 0 === t)
                throw new ReferenceError(
                  "this hasn't been initialised - super() hasn't been called",
                );
              return t;
            })(t);
          })(this, n);
        };
      }
      function I(t) {
        return (
          (I = Object.setPrototypeOf
            ? Object.getPrototypeOf.bind()
            : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t);
              }),
          I(t)
        );
      }
      var R = (function (t) {
        !(function (t, e) {
          if ("function" !== typeof e && null !== e)
            throw new TypeError(
              "Super expression must either be null or a function",
            );
          (t.prototype = Object.create(e && e.prototype, {
            constructor: { value: t, writable: !0, configurable: !0 },
          })),
            Object.defineProperty(t, "prototype", { writable: !1 }),
            e && L(t, e);
        })(c, t);
        var e,
          n,
          r,
          a = D(c);
        function c(t) {
          var e;
          return (
            (function (t, e) {
              if (!(t instanceof e))
                throw new TypeError("Cannot call a class as a function");
            })(this, c),
            ((e = a.call(this, t)).containerId = void 0),
            (e.portalRef = void 0),
            (e.containerRef = void 0),
            (e.shouldHandleWheel = void 0),
            (e.savePortalRef = function (t) {
              return (e.portalRef = t), t;
            }),
            (e.portalUpdate = function (t, n) {
              return e.portalRef.portalUpdate(t, n);
            }),
            (e.portalRegister = function () {
              return e.portalRef.portalRegister();
            }),
            (e.portalDeregister = function (t) {
              return e.portalRef.portalDeregister(t);
            }),
            (e.saveContainerRef = function (t) {
              return (
                o()(e.props.containerRef) && e.props.containerRef(t),
                (e.containerRef = t),
                t
              );
            }),
            (e.handleWheel = function (t) {
              return t.preventDefault();
            }),
            (e.containerId =
              i()(t) && void 0 !== t.containerId
                ? t.containerId
                : l()("victory-container-")),
            (e.shouldHandleWheel = !!(t && t.events && t.events.onWheel)),
            e
          );
        }
        return (
          (e = c),
          (n = [
            {
              key: "componentDidMount",
              value: function () {
                this.shouldHandleWheel &&
                  this.containerRef &&
                  this.containerRef.addEventListener("wheel", this.handleWheel);
              },
            },
            {
              key: "componentWillUnmount",
              value: function () {
                this.shouldHandleWheel &&
                  this.containerRef &&
                  this.containerRef.removeEventListener(
                    "wheel",
                    this.handleWheel,
                  );
              },
            },
            {
              key: "getIdForElement",
              value: function (t) {
                return "".concat(this.containerId, "-").concat(t);
              },
            },
            {
              key: "getChildren",
              value: function (t) {
                return t.children;
              },
            },
            {
              key: "getOUIAProps",
              value: function (t) {
                var e = t.ouiaId,
                  n = t.ouiaSafe,
                  r = t.ouiaType;
                return M(
                  M(
                    M({}, e && { "data-ouia-component-id": e }),
                    r && { "data-ouia-component-type": r },
                  ),
                  void 0 !== n && { "data-ouia-safe": n },
                );
              },
            },
            {
              key: "renderContainer",
              value: function (t, e, n) {
                var r = t.title,
                  o = t.desc,
                  a = t.portalComponent,
                  i = t.className,
                  c = t.width,
                  l = t.height,
                  u = t.portalZIndex,
                  f = t.responsive,
                  h = this.getChildren(t),
                  v = f
                    ? { width: "100%", height: "100%" }
                    : { width: c, height: l },
                  y = p()(
                    {
                      pointerEvents: "none",
                      touchAction: "none",
                      position: "relative",
                    },
                    v,
                  ),
                  m = p()(
                    { zIndex: u, position: "absolute", top: 0, left: 0 },
                    v,
                  ),
                  g = p()({ pointerEvents: "all" }, v),
                  b = p()({ overflow: "visible" }, v),
                  x = {
                    width: c,
                    height: l,
                    viewBox: e.viewBox,
                    preserveAspectRatio: e.preserveAspectRatio,
                    style: b,
                  };
                return d.createElement(
                  S.w.Provider,
                  {
                    value: {
                      portalUpdate: this.portalUpdate,
                      portalRegister: this.portalRegister,
                      portalDeregister: this.portalDeregister,
                    },
                  },
                  d.createElement(
                    "div",
                    P(
                      {
                        style: s()({}, n, y),
                        className: i,
                        ref: this.saveContainerRef,
                      },
                      this.getOUIAProps(t),
                    ),
                    d.createElement(
                      "svg",
                      P({}, e, { style: g }),
                      r
                        ? d.createElement(
                            "title",
                            { id: this.getIdForElement("title") },
                            r,
                          )
                        : null,
                      o
                        ? d.createElement(
                            "desc",
                            { id: this.getIdForElement("desc") },
                            o,
                          )
                        : null,
                      h,
                    ),
                    d.createElement(
                      "div",
                      { style: m },
                      d.cloneElement(
                        a,
                        M(M({}, x), {}, { ref: this.savePortalRef }),
                      ),
                    ),
                  ),
                );
              },
            },
            {
              key: "render",
              value: function () {
                var t = this.props,
                  e = t.width,
                  n = t.height,
                  r = t.responsive,
                  o = t.events,
                  a = t.title,
                  i = t.desc,
                  c = t.tabIndex,
                  l = t.preserveAspectRatio,
                  u = t.role,
                  s = r
                    ? this.props.style
                    : j.CE(this.props.style, ["height", "width"]),
                  f = k.I(this.props),
                  d = p()(
                    M(
                      {
                        width: e,
                        height: n,
                        tabIndex: c,
                        role: u,
                        "aria-labelledby":
                          [
                            a && this.getIdForElement("title"),
                            this.props["aria-labelledby"],
                          ]
                            .filter(Boolean)
                            .join(" ") || void 0,
                        "aria-describedby":
                          [
                            i && this.getIdForElement("desc"),
                            this.props["aria-describedby"],
                          ]
                            .filter(Boolean)
                            .join(" ") || void 0,
                        viewBox: r ? "0 0 ".concat(e, " ").concat(n) : void 0,
                        preserveAspectRatio: r ? l : void 0,
                      },
                      f,
                    ),
                    o,
                  );
                return this.renderContainer(this.props, d, s);
              },
            },
          ]) && _(e.prototype, n),
          r && _(e, r),
          Object.defineProperty(e, "prototype", { writable: !1 }),
          c
        );
      })(d.Component);
      (R.displayName = "VictoryContainer"),
        (R.role = "container"),
        (R.propTypes = {
          "aria-describedby": v().string,
          "aria-labelledby": v().string,
          children: v().oneOfType([v().arrayOf(v().node), v().node]),
          className: v().string,
          containerId: v().oneOfType([v().number, v().string]),
          containerRef: v().func,
          desc: v().string,
          events: v().object,
          height: y.A7,
          name: v().string,
          origin: v().shape({ x: y.A7, y: y.A7 }),
          ouiaId: v().oneOfType([v().number, v().string]),
          ouiaSafe: v().bool,
          ouiaType: v().string,
          polar: v().bool,
          portalComponent: v().element,
          portalZIndex: y._L,
          preserveAspectRatio: v().string,
          responsive: v().bool,
          role: v().string,
          style: v().object,
          tabIndex: v().number,
          theme: v().object,
          title: v().string,
          width: y.A7,
        }),
        (R.defaultProps = {
          className: "VictoryContainer",
          portalComponent: d.createElement(C, null),
          portalZIndex: 99,
          responsive: !0,
          role: "img",
        }),
        (R.contextType = A.Z);
    },
    83485: (t, e, n) => {
      "use strict";
      n.d(e, { X: () => U });
      var r = n(66364),
        o = n.n(r),
        a = n(66933),
        i = n.n(a),
        c = n(15687),
        l = n.n(c),
        u = n(52007),
        s = n.n(u),
        f = n(72791),
        p = n(41913),
        d = n(43350),
        h = ["children", "title", "desc"];
      function v(t, e) {
        if (null == t) return {};
        var n,
          r,
          o = (function (t, e) {
            if (null == t) return {};
            var n,
              r,
              o = {},
              a = Object.keys(t);
            for (r = 0; r < a.length; r++)
              (n = a[r]), e.indexOf(n) >= 0 || (o[n] = t[n]);
            return o;
          })(t, e);
        if (Object.getOwnPropertySymbols) {
          var a = Object.getOwnPropertySymbols(t);
          for (r = 0; r < a.length; r++)
            (n = a[r]),
              e.indexOf(n) >= 0 ||
                (Object.prototype.propertyIsEnumerable.call(t, n) &&
                  (o[n] = t[n]));
        }
        return o;
      }
      var y = function (t) {
        var e = t.children,
          n = t.title,
          r = t.desc,
          o = v(t, h);
        return f.createElement(
          "text",
          o,
          n && f.createElement("title", null, n),
          r && f.createElement("desc", null, r),
          e,
        );
      };
      y.propTypes = { children: s().node, desc: s().string, title: s().string };
      var m = function (t) {
          return f.createElement("tspan", t);
        },
        g = n(8091),
        b = n(21222),
        x = n(40143),
        O = n(42745),
        w = n(30637),
        C = n(62795),
        S = n(97409);
      function A(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function j(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? A(Object(n), !0).forEach(function (e) {
                k(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : A(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function k(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      function P(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return E(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return E(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return E(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function E(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      var M = {
          fill: "#252525",
          fontSize: 14,
          fontFamily:
            "'Gill Sans', 'Gill Sans MT', 'Ser\xadavek', 'Trebuchet MS', sans-serif",
          stroke: "transparent",
        },
        T = function (t, e) {
          return t.datum ? g.q2(t, t.datum)[e] : 0;
        },
        _ = function (t) {
          var e = t && t.fontSize;
          if ("number" === typeof e) return e;
          if (void 0 === e || null === e) return M.fontSize;
          if ("string" === typeof e) {
            var n = Number(e.replace("px", ""));
            return isNaN(n)
              ? (x.Z("fontSize should be expressed as a number of pixels"),
                M.fontSize)
              : n;
          }
          return M.fontSize;
        },
        L = function (t) {
          var e =
            arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 0;
          return Array.isArray(t) ? t[e] || t[0] : t;
        },
        D = function (t) {
          var e = t.backgroundStyle,
            n = t.backgroundPadding;
          return (Array.isArray(e) && !o()(e)) || (Array.isArray(n) && !o()(n));
        },
        I = function (t, e) {
          var n = t.direction,
            r = t.textAnchor,
            o = t.x,
            a = t.dx;
          if ("rtl" === n) return o - e;
          switch (r) {
            case "middle":
              return Math.round(o - e / 2);
            case "end":
              return Math.round(o - e);
            default:
              return o + (a || 0);
          }
        },
        R = function (t, e) {
          var n = t.verticalAnchor,
            r = t.y,
            o = t.originalDy,
            a = r + (void 0 === o ? 0 : o);
          switch (n) {
            case "start":
              return Math.floor(a);
            case "end":
              return Math.ceil(a - e);
            default:
              return Math.floor(a - e / 2);
          }
        },
        N = function (t, e) {
          return D(t)
            ? (function (t, e) {
                var n = t.dy,
                  r = t.dx,
                  o = t.transform,
                  a = t.backgroundStyle,
                  c = t.backgroundPadding,
                  l = t.backgroundComponent,
                  u = t.inline,
                  s = t.y,
                  p = e.map(function (t, o) {
                    var a = L(e, o - 1),
                      i = t.textSize,
                      l = t.fontSize * t.lineHeight,
                      f = Math.ceil(l),
                      p = L(c, o),
                      d = L(c, o - 1),
                      h = (u && r) || 0,
                      v =
                        o && !u
                          ? a.fontSize * a.lineHeight + d.top + d.bottom
                          : n - 0.5 * l - (t.fontSize - t.capHeight);
                    return {
                      textHeight: f,
                      labelSize: i,
                      heightWithPadding: f + p.top + p.bottom,
                      widthWithPadding: i.width + p.left + p.right + h,
                      y: s,
                      fontSize: t.fontSize,
                      dy: v,
                    };
                  });
                return p.map(function (e, n) {
                  var r = I(t, e.labelSize.width),
                    d = p.slice(0, n + 1).reduce(function (t, e) {
                      return t + e.dy;
                    }, s),
                    h = L(c, n),
                    v = e.heightWithPadding,
                    y = u
                      ? (function (t, e, n) {
                          var r = t.textAnchor,
                            o = e.map(function (t) {
                              return t.widthWithPadding;
                            }),
                            a =
                              -o.reduce(function (t, e) {
                                return t + e;
                              }, 0) / 2;
                          switch (r) {
                            case "start":
                              return o.reduce(function (t, e, r) {
                                return r < n ? t + e : t;
                              }, 0);
                            case "end":
                              return o.reduce(function (t, e, r) {
                                return r > n ? t - e : t;
                              }, 0);
                            default:
                              return o.reduce(function (t, e, r) {
                                return r === n
                                  ? t + e / 2
                                  : t + (r < n ? e : 0);
                              }, a);
                          }
                        })(t, p, n) +
                        r -
                        h.left
                      : r,
                    m = u ? R(t, v) - h.top : d,
                    g = {
                      key: "tspan-background-".concat(n),
                      height: v,
                      style: L(a, n),
                      width: e.widthWithPadding,
                      transform: o,
                      x: y - h.left,
                      y: m,
                    };
                  return f.cloneElement(l, i()({}, l.props, g));
                });
              })(t, e)
            : (function (t, e) {
                var n = t.dx,
                  r = void 0 === n ? 0 : n,
                  o = t.transform,
                  a = t.backgroundComponent,
                  c = t.backgroundStyle,
                  l = t.inline,
                  u = t.backgroundPadding,
                  s = t.capHeight,
                  p = e.map(function (t) {
                    return t.textSize;
                  }),
                  d = l
                    ? Math.max.apply(
                        Math,
                        P(
                          p.map(function (t) {
                            return t.height;
                          }),
                        ),
                      )
                    : p.reduce(function (t, n, r) {
                        var o = r ? 0 : s / 2;
                        return t + n.height * (e[r].lineHeight - o);
                      }, 0),
                  h = l
                    ? p.reduce(function (t, e, n) {
                        var o = n ? r : 0;
                        return t + e.width + o;
                      }, 0)
                    : Math.max.apply(
                        Math,
                        P(
                          p.map(function (t) {
                            return t.width;
                          }),
                        ),
                      ),
                  v = I(t, h),
                  y = R(t, d),
                  m = {
                    key: "background",
                    height: d + u.top + u.bottom,
                    style: c,
                    transform: o,
                    width: h + u.left + u.right,
                    x: l ? v - u.left : v + r - u.left,
                    y: y,
                  };
                return f.cloneElement(a, i()({}, a.props, m));
              })(t, e);
        },
        W = function (t, e, n) {
          var r = e.inline,
            o = L(t, n);
          return n && !r
            ? (function (t, e, n) {
                var r = L(t, e),
                  o = L(t, e - 1),
                  a = o.fontSize * o.lineHeight,
                  i = r.fontSize * r.lineHeight,
                  c = o.fontSize - o.capHeight,
                  l = r.fontSize - r.capHeight,
                  u =
                    a -
                    o.fontSize / 2 +
                    r.fontSize / 2 -
                    a / 2 +
                    i / 2 -
                    l / 2 +
                    c / 2;
                return D(n)
                  ? u + r.backgroundPadding.top + o.backgroundPadding.bottom
                  : u;
              })(t, n, e)
            : r
              ? 0 === n
                ? o.backgroundPadding.top
                : void 0
              : o.backgroundPadding.top;
        },
        F = function (t) {
          var e = (function (t, e) {
              if (void 0 !== t && null !== t) {
                if (Array.isArray(t))
                  return t.map(function (t) {
                    return g.xs(t, e);
                  });
                var n = g.xs(t, e);
                if (void 0 !== n && null !== n)
                  return Array.isArray(n) ? n : "".concat(n).split("\n");
              }
            })(t.text, t),
            n = (function (t, e) {
              if (e.disableInlineStyles) {
                var n = g.F3(t, e);
                return { fontSize: _(n) };
              }
              var r = function (t) {
                t = t ? i()({}, t, M) : M;
                var n = g.F3(t, e);
                return l()({}, n, { fontSize: _(n) });
              };
              return Array.isArray(t) && !o()(t)
                ? t.map(function (t) {
                    return r(t);
                  })
                : r(t);
            })(t.style, l()({}, t, { text: e })),
            r = (function (t, e) {
              if (t)
                return Array.isArray(t) && !o()(t)
                  ? t.map(function (t) {
                      return g.F3(t, e);
                    })
                  : g.F3(t, e);
            })(t.backgroundStyle, l()({}, t, { text: e, style: n })),
            a = (function (t) {
              if (t.backgroundPadding && Array.isArray(t.backgroundPadding))
                return t.backgroundPadding.map(function (e) {
                  var n = g.xs(e, t);
                  return g.tQ({ padding: n });
                });
              var e = g.xs(t.backgroundPadding, t);
              return g.tQ({ padding: e });
            })(l()({}, t, { text: e, style: n, backgroundStyle: r })),
            c = g.xs(t.id, t);
          return l()({}, t, {
            backgroundStyle: r,
            backgroundPadding: a,
            style: n,
            text: e,
            id: c,
          });
        },
        z = function (t) {
          var e = g.xs(t.ariaLabel, t),
            n = L(t.style),
            r = (function (t) {
              var e = g.xs(t.lineHeight, t);
              return Array.isArray(e) && o()(e) ? [1] : e;
            })(t),
            a = t.direction ? g.xs(t.direction, t) : "inherit",
            i = t.textAnchor ? g.xs(t.textAnchor, t) : n.textAnchor || "start",
            c = t.verticalAnchor
              ? g.xs(t.verticalAnchor, t)
              : n.verticalAnchor || "middle",
            u = t.dx ? g.xs(t.dx, t) : 0,
            s = (function (t, e, n) {
              var r = t.dy ? g.xs(t.dy, t) : 0,
                o = t.inline ? 1 : t.text.length,
                a = g.xs(t.capHeight, t),
                i = e ? g.xs(e, t) : "middle",
                c = P(Array(o).keys()).map(function (e) {
                  return L(t.style, e).fontSize;
                }),
                l = P(Array(o).keys()).map(function (t) {
                  return L(n, t);
                });
              if ("start" === i) return r + (a / 2 + l[0] / 2) * c[0];
              if (t.inline)
                return "end" === i
                  ? r + (a / 2 - l[0] / 2) * c[0]
                  : r + (a / 2) * c[0];
              if (1 === o)
                return "end" === i
                  ? r + (a / 2 + (0.5 - o) * l[0]) * c[0]
                  : r + (a / 2 + (0.5 - o / 2) * l[0]) * c[0];
              var u = P(Array(o).keys()).reduce(function (t, e) {
                return t + ((a / 2 + (0.5 - o) * l[e]) * c[e]) / o;
              }, 0);
              return "end" === i
                ? r + u
                : r + u / 2 + (a / 2) * l[o - 1] * c[o - 1];
            })(t, c, r),
            f = void 0 !== t.x ? t.x : T(t, "x"),
            p = void 0 !== t.y ? t.y : T(t, "y"),
            d = (function (t, e, n) {
              var r = t.polar,
                o = L(t.style),
                a = r ? b.Sw(t) : 0,
                i = void 0 === o.angle ? g.xs(t.angle, t) : o.angle,
                c = void 0 === i ? a : i,
                l = t.transform || o.transform,
                u = l && g.xs(l, t),
                s = c && { rotate: [c, e, n] };
              return u || c ? w._(u, s) : void 0;
            })(t, f, p);
          return l()({}, t, {
            ariaLabel: e,
            lineHeight: r,
            direction: a,
            textAnchor: i,
            verticalAnchor: c,
            dx: u,
            dy: s,
            originalDy: t.dy,
            transform: d,
            x: f,
            y: p,
          });
        },
        U = function (t) {
          if (null === (t = F(t)).text || void 0 === t.text) return null;
          var e = z(t),
            n = e.text,
            r = e.style,
            o = e.capHeight,
            a = e.backgroundPadding,
            i = e.lineHeight,
            c = n.map(function (t, e) {
              var n = L(r, e),
                c = C.Tj("".concat(o, "em"), n.fontSize),
                l = L(i, e);
              return {
                style: n,
                fontSize: n.fontSize || M.fontSize,
                capHeight: c,
                text: t,
                textSize: C.Z9(t, n),
                lineHeight: l,
                backgroundPadding: L(a, e),
              };
            }),
            l = (function (t, e) {
              var n = t.ariaLabel,
                r = t.inline,
                o = t.className,
                a = t.title,
                i = t.events,
                c = t.direction,
                l = t.text,
                u = t.textAnchor,
                s = t.dx,
                p = t.dy,
                d = t.transform,
                h = t.x,
                v = t.y,
                y = t.desc,
                m = t.id,
                b = t.tabIndex,
                x = t.tspanComponent,
                O = t.textComponent,
                w = S.I(t),
                C = j(
                  j({ "aria-label": n, key: "text" }, i),
                  {},
                  {
                    direction: c,
                    dx: s,
                    x: h,
                    y: v + p,
                    transform: d,
                    className: o,
                    title: a,
                    desc: g.xs(y, t),
                    tabIndex: g.xs(b, t),
                    id: m,
                  },
                  w,
                ),
                A = l.map(function (n, o) {
                  var a = e[o].style,
                    i = {
                      key: "".concat(m, "-key-").concat(o),
                      x: r ? void 0 : h,
                      dx: r ? s + e[o].backgroundPadding.left : s,
                      dy: W(e, t, o),
                      textAnchor: a.textAnchor || u,
                      style: a,
                      children: n,
                    };
                  return f.cloneElement(x, i);
                });
              return f.cloneElement(O, C, A);
            })(e, c);
          if (t.backgroundStyle) {
            var u = [N(e, c), l],
              s = f.cloneElement(t.groupComponent, {}, u);
            return t.renderInPortal ? f.createElement(p.V, null, s) : s;
          }
          return t.renderInPortal ? f.createElement(p.V, null, l) : l;
        };
      (U.displayName = "VictoryLabel"),
        (U.role = "label"),
        (U.defaultStyles = M),
        (U.propTypes = {
          active: s().bool,
          angle: s().oneOfType([s().string, s().number, s().func]),
          ariaLabel: s().oneOfType([s().string, s().func]),
          backgroundComponent: s().element,
          backgroundPadding: s().oneOfType([s().number, s().object, s().array]),
          backgroundStyle: s().oneOfType([s().object, s().array]),
          capHeight: s().oneOfType([s().string, O.A7, s().func]),
          className: s().string,
          data: s().array,
          datum: s().any,
          desc: s().oneOfType([s().string, s().func]),
          direction: s().oneOf(["rtl", "ltr", "inherit"]),
          dx: s().oneOfType([s().number, s().string, s().func]),
          dy: s().oneOfType([s().number, s().string, s().func]),
          events: s().object,
          groupComponent: s().element,
          id: s().oneOfType([s().number, s().string, s().func]),
          index: s().oneOfType([s().number, s().string]),
          inline: s().bool,
          labelPlacement: s().oneOf(["parallel", "perpendicular", "vertical"]),
          lineHeight: s().oneOfType([s().string, O.A7, s().func, s().array]),
          origin: s().shape({ x: O.A7.isRequired, y: O.A7.isRequired }),
          polar: s().bool,
          renderInPortal: s().bool,
          scale: s().shape({ x: O.bA, y: O.bA }),
          style: s().oneOfType([s().object, s().array]),
          tabIndex: s().oneOfType([s().number, s().func]),
          text: s().oneOfType([s().string, s().number, s().func, s().array]),
          textAnchor: s().oneOfType([
            s().oneOf(["start", "middle", "end", "inherit"]),
            s().func,
          ]),
          textComponent: s().element,
          title: s().string,
          transform: s().oneOfType([s().string, s().object, s().func]),
          tspanComponent: s().element,
          verticalAnchor: s().oneOfType([
            s().oneOf(["start", "middle", "end"]),
            s().func,
          ]),
          x: s().oneOfType([s().number, s().string]),
          y: s().oneOfType([s().number, s().string]),
        }),
        (U.defaultProps = {
          backgroundComponent: f.createElement(d.U, null),
          groupComponent: f.createElement("g", null),
          direction: "inherit",
          textComponent: f.createElement(y, null),
          tspanComponent: f.createElement(m, null),
          capHeight: 0.71,
          lineHeight: 1,
        });
    },
    64606: (t, e, n) => {
      "use strict";
      n.d(e, { w: () => r });
      var r = n(72791).createContext({});
      r.displayName = "PortalContext";
    },
    41913: (t, e, n) => {
      "use strict";
      n.d(e, { V: () => v });
      var r = n(66933),
        o = n.n(r),
        a = n(72791),
        i = n(52007),
        c = n.n(i),
        l = n(40143),
        u = n(8091),
        s = n(64606);
      function f(t, e) {
        for (var n = 0; n < e.length; n++) {
          var r = e[n];
          (r.enumerable = r.enumerable || !1),
            (r.configurable = !0),
            "value" in r && (r.writable = !0),
            Object.defineProperty(t, r.key, r);
        }
      }
      function p(t, e) {
        return (
          (p = Object.setPrototypeOf
            ? Object.setPrototypeOf.bind()
            : function (t, e) {
                return (t.__proto__ = e), t;
              }),
          p(t, e)
        );
      }
      function d(t) {
        var e = (function () {
          if ("undefined" === typeof Reflect || !Reflect.construct) return !1;
          if (Reflect.construct.sham) return !1;
          if ("function" === typeof Proxy) return !0;
          try {
            return (
              Boolean.prototype.valueOf.call(
                Reflect.construct(Boolean, [], function () {}),
              ),
              !0
            );
          } catch (t) {
            return !1;
          }
        })();
        return function () {
          var n,
            r = h(t);
          if (e) {
            var o = h(this).constructor;
            n = Reflect.construct(r, arguments, o);
          } else n = r.apply(this, arguments);
          return (function (t, e) {
            if (e && ("object" === typeof e || "function" === typeof e))
              return e;
            if (void 0 !== e)
              throw new TypeError(
                "Derived constructors may only return object or undefined",
              );
            return (function (t) {
              if (void 0 === t)
                throw new ReferenceError(
                  "this hasn't been initialised - super() hasn't been called",
                );
              return t;
            })(t);
          })(this, n);
        };
      }
      function h(t) {
        return (
          (h = Object.setPrototypeOf
            ? Object.getPrototypeOf.bind()
            : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t);
              }),
          h(t)
        );
      }
      var v = (function (t) {
        !(function (t, e) {
          if ("function" !== typeof e && null !== e)
            throw new TypeError(
              "Super expression must either be null or a function",
            );
          (t.prototype = Object.create(e && e.prototype, {
            constructor: { value: t, writable: !0, configurable: !0 },
          })),
            Object.defineProperty(t, "prototype", { writable: !1 }),
            e && p(t, e);
        })(c, t);
        var e,
          n,
          r,
          i = d(c);
        function c() {
          var t;
          !(function (t, e) {
            if (!(t instanceof e))
              throw new TypeError("Cannot call a class as a function");
          })(this, c);
          for (var e = arguments.length, n = new Array(e), r = 0; r < e; r++)
            n[r] = arguments[r];
          return (
            ((t = i.call.apply(i, [this].concat(n))).checkedContext = void 0),
            (t.renderInPlace = void 0),
            (t.element = void 0),
            (t.portalKey = void 0),
            t
          );
        }
        return (
          (e = c),
          (n = [
            {
              key: "componentDidMount",
              value: function () {
                this.checkedContext ||
                  ("function" !== typeof this.context.portalUpdate &&
                    (l.Z(
                      "`renderInPortal` is not supported outside of `VictoryContainer`. Component will be rendered in place",
                    ),
                    (this.renderInPlace = !0)),
                  (this.checkedContext = !0)),
                  this.forceUpdate();
              },
            },
            {
              key: "componentDidUpdate",
              value: function () {
                this.renderInPlace ||
                  ((this.portalKey =
                    this.portalKey || this.context.portalRegister()),
                  this.context.portalUpdate(this.portalKey, this.element));
              },
            },
            {
              key: "componentWillUnmount",
              value: function () {
                this.context &&
                  this.context.portalDeregister &&
                  this.context.portalDeregister(this.portalKey);
              },
            },
            {
              key: "renderPortal",
              value: function (t) {
                return this.renderInPlace ? t : ((this.element = t), null);
              },
            },
            {
              key: "render",
              value: function () {
                var t = Array.isArray(this.props.children)
                    ? this.props.children[0]
                    : this.props.children,
                  e = this.props.groupComponent,
                  n = (t && t.props) || {},
                  r = n.groupComponent
                    ? { groupComponent: e, standalone: !1 }
                    : {},
                  i = o()(
                    r,
                    n,
                    u.CE(this.props, ["children", "groupComponent"]),
                  ),
                  c = t && a.cloneElement(t, i);
                return this.renderPortal(c);
              },
            },
          ]) && f(e.prototype, n),
          r && f(e, r),
          Object.defineProperty(e, "prototype", { writable: !1 }),
          c
        );
      })(a.Component);
      (v.displayName = "VictoryPortal"),
        (v.role = "portal"),
        (v.propTypes = { children: c().node, groupComponent: c().element }),
        (v.defaultProps = { groupComponent: a.createElement("g", null) }),
        (v.contextType = s.w);
    },
    53841: (t, e, n) => {
      "use strict";
      n.d(e, { c: () => m });
      var r = n(15687),
        o = n.n(r),
        a = n(72791),
        i = n(52007),
        c = n.n(i),
        l = n(8091),
        u = n(46577),
        s = ["desc"];
      function f() {
        return (
          (f = Object.assign
            ? Object.assign.bind()
            : function (t) {
                for (var e = 1; e < arguments.length; e++) {
                  var n = arguments[e];
                  for (var r in n)
                    Object.prototype.hasOwnProperty.call(n, r) && (t[r] = n[r]);
                }
                return t;
              }),
          f.apply(this, arguments)
        );
      }
      function p(t, e) {
        if (null == t) return {};
        var n,
          r,
          o = (function (t, e) {
            if (null == t) return {};
            var n,
              r,
              o = {},
              a = Object.keys(t);
            for (r = 0; r < a.length; r++)
              (n = a[r]), e.indexOf(n) >= 0 || (o[n] = t[n]);
            return o;
          })(t, e);
        if (Object.getOwnPropertySymbols) {
          var a = Object.getOwnPropertySymbols(t);
          for (r = 0; r < a.length; r++)
            (n = a[r]),
              e.indexOf(n) >= 0 ||
                (Object.prototype.propertyIsEnumerable.call(t, n) &&
                  (o[n] = t[n]));
        }
        return o;
      }
      var d = function (t) {
        var e = t.desc,
          n = p(t, s);
        return e
          ? a.createElement(
              "line",
              f({ vectorEffect: "non-scaling-stroke" }, n),
              a.createElement("desc", null, e),
            )
          : a.createElement(
              "line",
              f({ vectorEffect: "non-scaling-stroke" }, n),
            );
      };
      function h(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function v(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? h(Object(n), !0).forEach(function (e) {
                y(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : h(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function y(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      var m = function (t) {
        return (
          (t = (function (t) {
            var e = l.xs(t.ariaLabel, t),
              n = l.xs(t.desc, t),
              r = l.xs(t.id, t),
              a = l.F3(o()({ stroke: "black" }, t.style), t),
              i = l.xs(t.tabIndex, t);
            return o()({}, t, {
              ariaLabel: e,
              desc: n,
              id: r,
              style: a,
              tabIndex: i,
            });
          })(t)),
          a.cloneElement(
            t.lineComponent,
            v(
              v({}, t.events),
              {},
              {
                "aria-label": t.ariaLabel,
                style: t.style,
                desc: t.desc,
                tabIndex: t.tabIndex,
                className: t.className,
                role: t.role,
                shapeRendering: t.shapeRendering,
                x1: t.x1,
                x2: t.x2,
                y1: t.y1,
                y2: t.y2,
                transform: t.transform,
                clipPath: t.clipPath,
              },
            ),
          )
        );
      };
      (m.propTypes = v(
        v({}, u.l.primitiveProps),
        {},
        {
          datum: c().any,
          lineComponent: c().element,
          x1: c().number,
          x2: c().number,
          y1: c().number,
          y2: c().number,
        },
      )),
        (m.defaultProps = {
          lineComponent: a.createElement(d, null),
          role: "presentation",
          shapeRendering: "auto",
        });
    },
    42017: (t, e, n) => {
      "use strict";
      n.d(e, { y: () => c });
      var r = n(72791),
        o = ["desc"];
      function a() {
        return (
          (a = Object.assign
            ? Object.assign.bind()
            : function (t) {
                for (var e = 1; e < arguments.length; e++) {
                  var n = arguments[e];
                  for (var r in n)
                    Object.prototype.hasOwnProperty.call(n, r) && (t[r] = n[r]);
                }
                return t;
              }),
          a.apply(this, arguments)
        );
      }
      function i(t, e) {
        if (null == t) return {};
        var n,
          r,
          o = (function (t, e) {
            if (null == t) return {};
            var n,
              r,
              o = {},
              a = Object.keys(t);
            for (r = 0; r < a.length; r++)
              (n = a[r]), e.indexOf(n) >= 0 || (o[n] = t[n]);
            return o;
          })(t, e);
        if (Object.getOwnPropertySymbols) {
          var a = Object.getOwnPropertySymbols(t);
          for (r = 0; r < a.length; r++)
            (n = a[r]),
              e.indexOf(n) >= 0 ||
                (Object.prototype.propertyIsEnumerable.call(t, n) &&
                  (o[n] = t[n]));
        }
        return o;
      }
      var c = (0, r.forwardRef)(function (t, e) {
        var n = t.desc,
          c = i(t, o);
        return n
          ? r.createElement(
              "path",
              a({}, c, { ref: e }),
              r.createElement("desc", null, n),
            )
          : r.createElement("path", a({}, c, { ref: e }));
      });
    },
    43350: (t, e, n) => {
      "use strict";
      n.d(e, { U: () => c });
      var r = n(72791),
        o = ["desc"];
      function a() {
        return (
          (a = Object.assign
            ? Object.assign.bind()
            : function (t) {
                for (var e = 1; e < arguments.length; e++) {
                  var n = arguments[e];
                  for (var r in n)
                    Object.prototype.hasOwnProperty.call(n, r) && (t[r] = n[r]);
                }
                return t;
              }),
          a.apply(this, arguments)
        );
      }
      function i(t, e) {
        if (null == t) return {};
        var n,
          r,
          o = (function (t, e) {
            if (null == t) return {};
            var n,
              r,
              o = {},
              a = Object.keys(t);
            for (r = 0; r < a.length; r++)
              (n = a[r]), e.indexOf(n) >= 0 || (o[n] = t[n]);
            return o;
          })(t, e);
        if (Object.getOwnPropertySymbols) {
          var a = Object.getOwnPropertySymbols(t);
          for (r = 0; r < a.length; r++)
            (n = a[r]),
              e.indexOf(n) >= 0 ||
                (Object.prototype.propertyIsEnumerable.call(t, n) &&
                  (o[n] = t[n]));
        }
        return o;
      }
      var c = function (t) {
        var e = t.desc,
          n = i(t, o);
        return e
          ? r.createElement(
              "rect",
              a({ vectorEffect: "non-scaling-stroke" }, n),
              r.createElement("desc", null, e),
            )
          : r.createElement(
              "rect",
              a({ vectorEffect: "non-scaling-stroke" }, n),
            );
      };
    },
    58853: (t, e, n) => {
      "use strict";
      n.d(e, { J: () => w });
      var r = n(15687),
        o = n.n(r),
        a = [
          "#252525",
          "#525252",
          "#737373",
          "#969696",
          "#bdbdbd",
          "#d9d9d9",
          "#f0f0f0",
        ],
        i = "#252525",
        c = "#969696",
        l = { width: 450, height: 300, padding: 50, colorScale: a },
        u = {
          fontFamily: "'Gill Sans', 'Seravek', 'Trebuchet MS', sans-serif",
          fontSize: 14,
          letterSpacing: "normal",
          padding: 10,
          fill: i,
          stroke: "transparent",
        },
        s = o()({ textAnchor: "middle" }, u),
        f = {
          area: o()({ style: { data: { fill: i }, labels: u } }, l),
          axis: o()(
            {
              style: {
                axis: {
                  fill: "transparent",
                  stroke: i,
                  strokeWidth: 1,
                  strokeLinecap: "round",
                  strokeLinejoin: "round",
                },
                axisLabel: o()({}, s, { padding: 25 }),
                grid: {
                  fill: "none",
                  stroke: "none",
                  pointerEvents: "painted",
                },
                ticks: { fill: "transparent", size: 1, stroke: "transparent" },
                tickLabels: u,
              },
            },
            l,
          ),
          bar: o()(
            {
              style: {
                data: { fill: i, padding: 8, strokeWidth: 0 },
                labels: u,
              },
            },
            l,
          ),
          boxplot: o()(
            {
              style: {
                max: { padding: 8, stroke: i, strokeWidth: 1 },
                maxLabels: o()({}, u, { padding: 3 }),
                median: { padding: 8, stroke: i, strokeWidth: 1 },
                medianLabels: o()({}, u, { padding: 3 }),
                min: { padding: 8, stroke: i, strokeWidth: 1 },
                minLabels: o()({}, u, { padding: 3 }),
                q1: { padding: 8, fill: c },
                q1Labels: o()({}, u, { padding: 3 }),
                q3: { padding: 8, fill: c },
                q3Labels: o()({}, u, { padding: 3 }),
              },
              boxWidth: 20,
            },
            l,
          ),
          candlestick: o()(
            {
              style: {
                data: { stroke: i, strokeWidth: 1 },
                labels: o()({}, u, { padding: 5 }),
              },
              candleColors: { positive: "#ffffff", negative: i },
            },
            l,
          ),
          chart: l,
          errorbar: o()(
            {
              borderWidth: 8,
              style: {
                data: { fill: "transparent", stroke: i, strokeWidth: 2 },
                labels: u,
              },
            },
            l,
          ),
          group: o()({ colorScale: a }, l),
          histogram: o()(
            {
              style: {
                data: { fill: c, stroke: i, strokeWidth: 2 },
                labels: u,
              },
            },
            l,
          ),
          legend: {
            colorScale: a,
            gutter: 10,
            orientation: "vertical",
            titleOrientation: "top",
            style: {
              data: { type: "circle" },
              labels: u,
              title: o()({}, u, { padding: 5 }),
            },
          },
          line: o()(
            {
              style: {
                data: { fill: "transparent", stroke: i, strokeWidth: 2 },
                labels: u,
              },
            },
            l,
          ),
          pie: {
            style: {
              data: { padding: 10, stroke: "transparent", strokeWidth: 1 },
              labels: o()({}, u, { padding: 20 }),
            },
            colorScale: a,
            width: 400,
            height: 400,
            padding: 50,
          },
          scatter: o()(
            {
              style: {
                data: { fill: i, stroke: "transparent", strokeWidth: 0 },
                labels: u,
              },
            },
            l,
          ),
          stack: o()({ colorScale: a }, l),
          tooltip: {
            style: o()({}, u, { padding: 0, pointerEvents: "none" }),
            flyoutStyle: {
              stroke: i,
              strokeWidth: 1,
              fill: "#f0f0f0",
              pointerEvents: "none",
            },
            flyoutPadding: 5,
            cornerRadius: 5,
            pointerLength: 10,
          },
          voronoi: o()(
            {
              style: {
                data: {
                  fill: "transparent",
                  stroke: "transparent",
                  strokeWidth: 0,
                },
                labels: o()({}, u, { padding: 5, pointerEvents: "none" }),
                flyout: {
                  stroke: i,
                  strokeWidth: 1,
                  fill: "#f0f0f0",
                  pointerEvents: "none",
                },
              },
            },
            l,
          ),
        },
        p = ["#F4511E", "#FFF59D", "#DCE775", "#8BC34A", "#00796B", "#006064"],
        d = "#ECEFF1",
        h = "#90A4AE",
        v = "#455A64",
        y = "#212121",
        m = { width: 350, height: 350, padding: 50 },
        g = {
          fontFamily: "'Helvetica Neue', 'Helvetica', sans-serif",
          fontSize: 12,
          letterSpacing: "normal",
          padding: 8,
          fill: v,
          stroke: "transparent",
          strokeWidth: 0,
        },
        b = o()({ textAnchor: "middle" }, g),
        x = "round",
        O = "round",
        w = {
          grayscale: f,
          material: {
            area: o()({ style: { data: { fill: y }, labels: g } }, m),
            axis: o()(
              {
                style: {
                  axis: {
                    fill: "transparent",
                    stroke: h,
                    strokeWidth: 2,
                    strokeLinecap: x,
                    strokeLinejoin: O,
                  },
                  axisLabel: o()({}, b, { padding: 8, stroke: "transparent" }),
                  grid: {
                    fill: "none",
                    stroke: d,
                    strokeDasharray: "10, 5",
                    strokeLinecap: x,
                    strokeLinejoin: O,
                    pointerEvents: "painted",
                  },
                  ticks: {
                    fill: "transparent",
                    size: 5,
                    stroke: h,
                    strokeWidth: 1,
                    strokeLinecap: x,
                    strokeLinejoin: O,
                  },
                  tickLabels: o()({}, g, { fill: v }),
                },
              },
              m,
            ),
            polarDependentAxis: o()({
              style: {
                ticks: { fill: "transparent", size: 1, stroke: "transparent" },
              },
            }),
            bar: o()(
              {
                style: {
                  data: { fill: v, padding: 8, strokeWidth: 0 },
                  labels: g,
                },
              },
              m,
            ),
            boxplot: o()(
              {
                style: {
                  max: { padding: 8, stroke: v, strokeWidth: 1 },
                  maxLabels: o()({}, g, { padding: 3 }),
                  median: { padding: 8, stroke: v, strokeWidth: 1 },
                  medianLabels: o()({}, g, { padding: 3 }),
                  min: { padding: 8, stroke: v, strokeWidth: 1 },
                  minLabels: o()({}, g, { padding: 3 }),
                  q1: { padding: 8, fill: v },
                  q1Labels: o()({}, g, { padding: 3 }),
                  q3: { padding: 8, fill: v },
                  q3Labels: o()({}, g, { padding: 3 }),
                },
                boxWidth: 20,
              },
              m,
            ),
            candlestick: o()(
              {
                style: {
                  data: { stroke: v },
                  labels: o()({}, g, { padding: 5 }),
                },
                candleColors: { positive: "#ffffff", negative: v },
              },
              m,
            ),
            chart: m,
            errorbar: o()(
              {
                borderWidth: 8,
                style: {
                  data: {
                    fill: "transparent",
                    opacity: 1,
                    stroke: v,
                    strokeWidth: 2,
                  },
                  labels: g,
                },
              },
              m,
            ),
            group: o()({ colorScale: p }, m),
            histogram: o()(
              {
                style: {
                  data: { fill: v, stroke: y, strokeWidth: 2 },
                  labels: g,
                },
              },
              m,
            ),
            legend: {
              colorScale: p,
              gutter: 10,
              orientation: "vertical",
              titleOrientation: "top",
              style: {
                data: { type: "circle" },
                labels: g,
                title: o()({}, g, { padding: 5 }),
              },
            },
            line: o()(
              {
                style: {
                  data: {
                    fill: "transparent",
                    opacity: 1,
                    stroke: v,
                    strokeWidth: 2,
                  },
                  labels: g,
                },
              },
              m,
            ),
            pie: o()(
              {
                colorScale: p,
                style: {
                  data: { padding: 8, stroke: d, strokeWidth: 1 },
                  labels: o()({}, g, { padding: 20 }),
                },
              },
              m,
            ),
            scatter: o()(
              {
                style: {
                  data: {
                    fill: v,
                    opacity: 1,
                    stroke: "transparent",
                    strokeWidth: 0,
                  },
                  labels: g,
                },
              },
              m,
            ),
            stack: o()({ colorScale: p }, m),
            tooltip: {
              style: o()({}, g, { padding: 0, pointerEvents: "none" }),
              flyoutStyle: {
                stroke: y,
                strokeWidth: 1,
                fill: "#f0f0f0",
                pointerEvents: "none",
              },
              flyoutPadding: 5,
              cornerRadius: 5,
              pointerLength: 10,
            },
            voronoi: o()(
              {
                style: {
                  data: {
                    fill: "transparent",
                    stroke: "transparent",
                    strokeWidth: 0,
                  },
                  labels: o()({}, g, { padding: 5, pointerEvents: "none" }),
                  flyout: {
                    stroke: y,
                    strokeWidth: 1,
                    fill: "#f0f0f0",
                    pointerEvents: "none",
                  },
                },
              },
              m,
            ),
          },
        };
    },
    86225: (t, e, n) => {
      "use strict";
      n.d(e, { o: () => Jt });
      var r = {};
      n.r(r),
        n.d(r, {
          easeBack: () => pt,
          easeBackIn: () => st,
          easeBackInOut: () => pt,
          easeBackOut: () => ft,
          easeBounce: () => ct,
          easeBounceIn: () => it,
          easeBounceInOut: () => lt,
          easeBounceOut: () => ct,
          easeCircle: () => K,
          easeCircleIn: () => Y,
          easeCircleInOut: () => K,
          easeCircleOut: () => Z,
          easeCubic: () => D,
          easeCubicIn: () => _,
          easeCubicInOut: () => D,
          easeCubicOut: () => L,
          easeElastic: () => vt,
          easeElasticIn: () => ht,
          easeElasticInOut: () => yt,
          easeElasticOut: () => vt,
          easeExp: () => $,
          easeExpIn: () => H,
          easeExpInOut: () => $,
          easeExpOut: () => V,
          easeLinear: () => P,
          easePoly: () => N,
          easePolyIn: () => I,
          easePolyInOut: () => N,
          easePolyOut: () => R,
          easeQuad: () => T,
          easeQuadIn: () => E,
          easeQuadInOut: () => T,
          easeQuadOut: () => M,
          easeSin: () => B,
          easeSinIn: () => z,
          easeSinInOut: () => B,
          easeSinOut: () => U,
        });
      var o = n(41761),
        a = n.n(o),
        i = n(36460),
        c = n.n(i),
        l = n(12742),
        u = n.n(l),
        s = n(42854),
        f = n.n(s),
        p = n(74786),
        d = n.n(p),
        h = n(66364),
        v = n.n(h),
        y = n(71180),
        m = n.n(y),
        g = n(66933),
        b = n.n(g),
        x = n(15687),
        O = n.n(x),
        w = n(72791),
        C = n(79704),
        S = n(50077),
        A = n.n(S),
        j = n(52007),
        k = n.n(j);
      const P = (t) => +t;
      function E(t) {
        return t * t;
      }
      function M(t) {
        return t * (2 - t);
      }
      function T(t) {
        return ((t *= 2) <= 1 ? t * t : --t * (2 - t) + 1) / 2;
      }
      function _(t) {
        return t * t * t;
      }
      function L(t) {
        return --t * t * t + 1;
      }
      function D(t) {
        return ((t *= 2) <= 1 ? t * t * t : (t -= 2) * t * t + 2) / 2;
      }
      var I = (function t(e) {
          function n(t) {
            return Math.pow(t, e);
          }
          return (e = +e), (n.exponent = t), n;
        })(3),
        R = (function t(e) {
          function n(t) {
            return 1 - Math.pow(1 - t, e);
          }
          return (e = +e), (n.exponent = t), n;
        })(3),
        N = (function t(e) {
          function n(t) {
            return (
              ((t *= 2) <= 1 ? Math.pow(t, e) : 2 - Math.pow(2 - t, e)) / 2
            );
          }
          return (e = +e), (n.exponent = t), n;
        })(3),
        W = Math.PI,
        F = W / 2;
      function z(t) {
        return 1 === +t ? 1 : 1 - Math.cos(t * F);
      }
      function U(t) {
        return Math.sin(t * F);
      }
      function B(t) {
        return (1 - Math.cos(W * t)) / 2;
      }
      function q(t) {
        return 1.0009775171065494 * (Math.pow(2, -10 * t) - 0.0009765625);
      }
      function H(t) {
        return q(1 - +t);
      }
      function V(t) {
        return 1 - q(t);
      }
      function $(t) {
        return ((t *= 2) <= 1 ? q(1 - t) : 2 - q(t - 1)) / 2;
      }
      function Y(t) {
        return 1 - Math.sqrt(1 - t * t);
      }
      function Z(t) {
        return Math.sqrt(1 - --t * t);
      }
      function K(t) {
        return (
          ((t *= 2) <= 1
            ? 1 - Math.sqrt(1 - t * t)
            : Math.sqrt(1 - (t -= 2) * t) + 1) / 2
        );
      }
      var G = 4 / 11,
        X = 6 / 11,
        Q = 8 / 11,
        J = 3 / 4,
        tt = 9 / 11,
        et = 10 / 11,
        nt = 15 / 16,
        rt = 21 / 22,
        ot = 63 / 64,
        at = 1 / G / G;
      function it(t) {
        return 1 - ct(1 - t);
      }
      function ct(t) {
        return (t = +t) < G
          ? at * t * t
          : t < Q
            ? at * (t -= X) * t + J
            : t < et
              ? at * (t -= tt) * t + nt
              : at * (t -= rt) * t + ot;
      }
      function lt(t) {
        return ((t *= 2) <= 1 ? 1 - ct(1 - t) : ct(t - 1) + 1) / 2;
      }
      var ut = 1.70158,
        st = (function t(e) {
          function n(t) {
            return (t = +t) * t * (e * (t - 1) + t);
          }
          return (e = +e), (n.overshoot = t), n;
        })(ut),
        ft = (function t(e) {
          function n(t) {
            return --t * t * ((t + 1) * e + t) + 1;
          }
          return (e = +e), (n.overshoot = t), n;
        })(ut),
        pt = (function t(e) {
          function n(t) {
            return (
              ((t *= 2) < 1
                ? t * t * ((e + 1) * t - e)
                : (t -= 2) * t * ((e + 1) * t + e) + 2) / 2
            );
          }
          return (e = +e), (n.overshoot = t), n;
        })(ut),
        dt = 2 * Math.PI,
        ht = (function t(e, n) {
          var r = Math.asin(1 / (e = Math.max(1, e))) * (n /= dt);
          function o(t) {
            return e * q(-(--t)) * Math.sin((r - t) / n);
          }
          return (
            (o.amplitude = function (e) {
              return t(e, n * dt);
            }),
            (o.period = function (n) {
              return t(e, n);
            }),
            o
          );
        })(1, 0.3),
        vt = (function t(e, n) {
          var r = Math.asin(1 / (e = Math.max(1, e))) * (n /= dt);
          function o(t) {
            return 1 - e * q((t = +t)) * Math.sin((t + r) / n);
          }
          return (
            (o.amplitude = function (e) {
              return t(e, n * dt);
            }),
            (o.period = function (n) {
              return t(e, n);
            }),
            o
          );
        })(1, 0.3),
        yt = (function t(e, n) {
          var r = Math.asin(1 / (e = Math.max(1, e))) * (n /= dt);
          function o(t) {
            return (
              ((t = 2 * t - 1) < 0
                ? e * q(-t) * Math.sin((r - t) / n)
                : 2 - e * q(t) * Math.sin((r + t) / n)) / 2
            );
          }
          return (
            (o.amplitude = function (e) {
              return t(e, n * dt);
            }),
            (o.period = function (n) {
              return t(e, n);
            }),
            o
          );
        })(1, 0.3),
        mt = n(45812),
        gt = n.n(mt),
        bt = n(93977),
        xt = n.n(bt),
        Ot = n(67536),
        wt = function (t) {
          if (null !== t)
            switch (typeof t) {
              case "undefined":
              case "boolean":
                return !1;
              case "number":
                return (
                  !isNaN(t) &&
                  t !== Number.POSITIVE_INFINITY &&
                  t !== Number.NEGATIVE_INFINITY
                );
              case "string":
              case "function":
                return !0;
              case "object":
                return t instanceof Date || Array.isArray(t) || xt()(t);
            }
          return !1;
        },
        Ct = function (t, e) {
          var n =
            arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : 0;
          return function (r) {
            return r < n ? t : e;
          };
        },
        St = function (t, e) {
          return function (n) {
            return n >= 1
              ? e
              : function () {
                  var r =
                      "function" === typeof t ? t.apply(this, arguments) : t,
                    o = "function" === typeof e ? e.apply(this, arguments) : e;
                  return (0, Ot.Z)(r, o)(n);
                };
          };
        },
        At = function (t, e) {
          var n,
            r,
            o,
            a = function (t) {
              return Array.isArray(t) ? gt()(t, "key") : t;
            },
            i = {},
            c = {};
          for (n in ((null !== t && "object" === typeof t) || (t = {}),
          (null !== e && "object" === typeof e) || (e = {}),
          e))
            n in t
              ? (i[n] =
                  ((r = a(t[n])),
                  (o = a(e[n])),
                  r !== o && wt(r) && wt(o)
                    ? "function" === typeof r || "function" === typeof o
                      ? St(r, o)
                      : ("object" === typeof r && xt()(r)) ||
                          ("object" === typeof o && xt()(o))
                        ? At(r, o)
                        : (0, Ot.Z)(r, o)
                    : Ct(r, o)))
              : (c[n] = e[n]);
          return function (t) {
            for (n in i) c[n] = i[n](t);
            return c;
          };
        },
        jt = function (t, e) {
          return t !== e && wt(t) && wt(e)
            ? "function" === typeof t || "function" === typeof e
              ? St(t, e)
              : xt()(t) || xt()(e)
                ? At(t, e)
                : "string" === typeof t || "string" === typeof e
                  ? (function (t, e) {
                      var n = function (t) {
                        return "string" === typeof t ? t.replace(/,/g, "") : t;
                      };
                      return (0, Ot.Z)(n(t), n(e));
                    })(t, e)
                  : (0, Ot.Z)(t, e)
            : Ct(t, e);
        },
        kt = n(91002);
      function Pt(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return Et(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return Et(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return Et(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function Et(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function Mt(t, e) {
        for (var n = 0; n < e.length; n++) {
          var r = e[n];
          (r.enumerable = r.enumerable || !1),
            (r.configurable = !0),
            "value" in r && (r.writable = !0),
            Object.defineProperty(t, r.key, r);
        }
      }
      function Tt(t, e) {
        return (
          (Tt = Object.setPrototypeOf
            ? Object.setPrototypeOf.bind()
            : function (t, e) {
                return (t.__proto__ = e), t;
              }),
          Tt(t, e)
        );
      }
      function _t(t) {
        var e = (function () {
          if ("undefined" === typeof Reflect || !Reflect.construct) return !1;
          if (Reflect.construct.sham) return !1;
          if ("function" === typeof Proxy) return !0;
          try {
            return (
              Boolean.prototype.valueOf.call(
                Reflect.construct(Boolean, [], function () {}),
              ),
              !0
            );
          } catch (t) {
            return !1;
          }
        })();
        return function () {
          var n,
            r = Lt(t);
          if (e) {
            var o = Lt(this).constructor;
            n = Reflect.construct(r, arguments, o);
          } else n = r.apply(this, arguments);
          return (function (t, e) {
            if (e && ("object" === typeof e || "function" === typeof e))
              return e;
            if (void 0 !== e)
              throw new TypeError(
                "Derived constructors may only return object or undefined",
              );
            return (function (t) {
              if (void 0 === t)
                throw new ReferenceError(
                  "this hasn't been initialised - super() hasn't been called",
                );
              return t;
            })(t);
          })(this, n);
        };
      }
      function Lt(t) {
        return (
          (Lt = Object.setPrototypeOf
            ? Object.getPrototypeOf.bind()
            : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t);
              }),
          Lt(t)
        );
      }
      var Dt = (function (t) {
        !(function (t, e) {
          if ("function" !== typeof e && null !== e)
            throw new TypeError(
              "Super expression must either be null or a function",
            );
          (t.prototype = Object.create(e && e.prototype, {
            constructor: { value: t, writable: !0, configurable: !0 },
          })),
            Object.defineProperty(t, "prototype", { writable: !1 }),
            e && Tt(t, e);
        })(i, t);
        var e,
          n,
          o,
          a = _t(i);
        function i(t, e) {
          var n;
          return (
            (function (t, e) {
              if (!(t instanceof e))
                throw new TypeError("Cannot call a class as a function");
            })(this, i),
            ((n = a.call(this, t, e)).interpolator = void 0),
            (n.queue = void 0),
            (n.ease = void 0),
            (n.timer = void 0),
            (n.loopID = void 0),
            (n.functionToBeRunEachFrame = function (t, e) {
              var r = (e = void 0 !== e ? e : n.props.duration) ? t / e : 1;
              if (r >= 1)
                return (
                  n.setState({
                    data: n.interpolator(1),
                    animationInfo: {
                      progress: 1,
                      animating: !1,
                      terminating: !0,
                    },
                  }),
                  n.loopID && n.timer.unsubscribe(n.loopID),
                  n.queue.shift(),
                  void n.traverseQueue()
                );
              n.setState({
                data: n.interpolator(n.ease(r)),
                animationInfo: { progress: r, animating: r < 1 },
              });
            }),
            (n.state = {
              data: Array.isArray(n.props.data)
                ? n.props.data[0]
                : n.props.data,
              animationInfo: { progress: 0, animating: !1 },
            }),
            (n.interpolator = null),
            (n.queue = Array.isArray(n.props.data)
              ? n.props.data.slice(1)
              : []),
            (n.ease = r[n.toNewName(n.props.easing)]),
            (n.timer = n.context.animationTimer),
            n
          );
        }
        return (
          (e = i),
          (n = [
            {
              key: "componentDidMount",
              value: function () {
                this.queue.length && this.traverseQueue();
              },
            },
            {
              key: "componentDidUpdate",
              value: function (t) {
                if (!A()(this.props, t))
                  if (
                    this.interpolator &&
                    this.state.animationInfo &&
                    this.state.animationInfo.progress < 1
                  )
                    this.setState({
                      data: this.interpolator(1),
                      animationInfo: {
                        progress: 1,
                        animating: !1,
                        terminating: !0,
                      },
                    });
                  else {
                    var e;
                    this.timer.unsubscribe(this.loopID),
                      Array.isArray(this.props.data)
                        ? (e = this.queue).push.apply(e, Pt(this.props.data))
                        : ((this.queue.length = 0),
                          this.queue.push(this.props.data)),
                      this.traverseQueue();
                  }
              },
            },
            {
              key: "componentWillUnmount",
              value: function () {
                this.loopID
                  ? this.timer.unsubscribe(this.loopID)
                  : this.timer.stop();
              },
            },
            {
              key: "toNewName",
              value: function (t) {
                var e;
                return "ease".concat(
                  (e = t) && e[0].toUpperCase() + e.slice(1),
                );
              },
            },
            {
              key: "traverseQueue",
              value: function () {
                var t = this;
                if (this.queue.length) {
                  var e = this.queue[0];
                  (this.interpolator = jt(this.state.data, e)),
                    this.props.delay
                      ? setTimeout(function () {
                          t.loopID = t.timer.subscribe(
                            t.functionToBeRunEachFrame,
                            t.props.duration,
                          );
                        }, this.props.delay)
                      : (this.loopID = this.timer.subscribe(
                          this.functionToBeRunEachFrame,
                          this.props.duration,
                        ));
                } else this.props.onEnd && this.props.onEnd();
              },
            },
            {
              key: "render",
              value: function () {
                return this.props.children(
                  this.state.data,
                  this.state.animationInfo,
                );
              },
            },
          ]) && Mt(e.prototype, n),
          o && Mt(e, o),
          Object.defineProperty(e, "prototype", { writable: !1 }),
          i
        );
      })(w.Component);
      (Dt.displayName = "VictoryAnimation"),
        (Dt.propTypes = {
          children: k().func,
          data: k().oneOfType([k().object, k().array]),
          delay: k().number,
          duration: k().number,
          easing: k().oneOf([
            "back",
            "backIn",
            "backOut",
            "backInOut",
            "bounce",
            "bounceIn",
            "bounceOut",
            "bounceInOut",
            "circle",
            "circleIn",
            "circleOut",
            "circleInOut",
            "linear",
            "linearIn",
            "linearOut",
            "linearInOut",
            "cubic",
            "cubicIn",
            "cubicOut",
            "cubicInOut",
            "elastic",
            "elasticIn",
            "elasticOut",
            "elasticInOut",
            "exp",
            "expIn",
            "expOut",
            "expInOut",
            "poly",
            "polyIn",
            "polyOut",
            "polyInOut",
            "quad",
            "quadIn",
            "quadOut",
            "quadInOut",
            "sin",
            "sinIn",
            "sinOut",
            "sinInOut",
          ]),
          onEnd: k().func,
        }),
        (Dt.defaultProps = {
          data: {},
          delay: 0,
          duration: 1e3,
          easing: "quadInOut",
        }),
        (Dt.contextType = kt.Z);
      var It = n(15896),
        Rt = n(8091),
        Nt = n(5129);
      function Wt() {
        return (
          (Wt = Object.assign
            ? Object.assign.bind()
            : function (t) {
                for (var e = 1; e < arguments.length; e++) {
                  var n = arguments[e];
                  for (var r in n)
                    Object.prototype.hasOwnProperty.call(n, r) && (t[r] = n[r]);
                }
                return t;
              }),
          Wt.apply(this, arguments)
        );
      }
      function Ft(t, e) {
        for (var n = 0; n < e.length; n++) {
          var r = e[n];
          (r.enumerable = r.enumerable || !1),
            (r.configurable = !0),
            "value" in r && (r.writable = !0),
            Object.defineProperty(t, r.key, r);
        }
      }
      function zt(t, e) {
        return (
          (zt = Object.setPrototypeOf
            ? Object.setPrototypeOf.bind()
            : function (t, e) {
                return (t.__proto__ = e), t;
              }),
          zt(t, e)
        );
      }
      function Ut(t) {
        var e = (function () {
          if ("undefined" === typeof Reflect || !Reflect.construct) return !1;
          if (Reflect.construct.sham) return !1;
          if ("function" === typeof Proxy) return !0;
          try {
            return (
              Boolean.prototype.valueOf.call(
                Reflect.construct(Boolean, [], function () {}),
              ),
              !0
            );
          } catch (t) {
            return !1;
          }
        })();
        return function () {
          var n,
            r = Bt(t);
          if (e) {
            var o = Bt(this).constructor;
            n = Reflect.construct(r, arguments, o);
          } else n = r.apply(this, arguments);
          return (function (t, e) {
            if (e && ("object" === typeof e || "function" === typeof e))
              return e;
            if (void 0 !== e)
              throw new TypeError(
                "Derived constructors may only return object or undefined",
              );
            return (function (t) {
              if (void 0 === t)
                throw new ReferenceError(
                  "this hasn't been initialised - super() hasn't been called",
                );
              return t;
            })(t);
          })(this, n);
        };
      }
      function Bt(t) {
        return (
          (Bt = Object.setPrototypeOf
            ? Object.getPrototypeOf.bind()
            : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t);
              }),
          Bt(t)
        );
      }
      var qt = (function (t) {
        !(function (t, e) {
          if ("function" !== typeof e && null !== e)
            throw new TypeError(
              "Super expression must either be null or a function",
            );
          (t.prototype = Object.create(e && e.prototype, {
            constructor: { value: t, writable: !0, configurable: !0 },
          })),
            Object.defineProperty(t, "prototype", { writable: !1 }),
            e && zt(t, e);
        })(a, t);
        var e,
          n,
          r,
          o = Ut(a);
        function a(t, e) {
          var n;
          !(function (t, e) {
            if (!(t instanceof e))
              throw new TypeError("Cannot call a class as a function");
          })(this, a),
            ((n = o.call(this, t, e)).continuous = void 0),
            (n.timer = void 0),
            (n.transitionProps = void 0),
            (n.state = { nodesShouldLoad: !1, nodesDoneLoad: !1 });
          var r = n.props.children,
            i = r.props.polar;
          return (
            (n.continuous = !i && r.type && !0 === r.type.continuous),
            (n.timer = n.context.transitionTimer),
            n
          );
        }
        return (
          (e = a),
          (n = [
            {
              key: "componentDidMount",
              value: function () {
                this.setState({ nodesShouldLoad: !0 });
              },
            },
            {
              key: "shouldComponentUpdate",
              value: function (t) {
                var e = this;
                return (
                  A()(this.props, t) ||
                    (this.timer.bypassAnimation(),
                    this.setState(
                      this.getTransitionState(this.props, t),
                      function () {
                        return e.timer.resumeAnimation();
                      },
                    )),
                  !0
                );
              },
            },
            {
              key: "componentWillUnmount",
              value: function () {
                this.timer.stop();
              },
            },
            {
              key: "getTransitionState",
              value: function (t, e) {
                var n = t.animate;
                if (!n) return {};
                if (n.parentState)
                  return {
                    oldProps: n.parentState.nodesWillExit ? t : null,
                    nextProps: e,
                  };
                var r = w.Children.toArray(t.children),
                  o = w.Children.toArray(e.children),
                  a = Nt.A(r, o),
                  i = a.nodesWillExit;
                return {
                  nodesWillExit: i,
                  nodesWillEnter: a.nodesWillEnter,
                  childrenTransitions: a.childrenTransitions,
                  nodesShouldEnter: a.nodesShouldEnter,
                  oldProps: i ? t : null,
                  nextProps: e,
                };
              },
            },
            {
              key: "getDomainFromChildren",
              value: function (t, e) {
                var n = function (t) {
                    return t.reduce(function (t, r) {
                      if (r.type && d()(r.type.getDomain)) {
                        var o = r.props && r.type.getDomain(r.props, e);
                        return o ? t.concat(o) : t;
                      }
                      return r.props && r.props.children
                        ? t.concat(n(w.Children.toArray(r.props.children)))
                        : t;
                    }, []);
                  },
                  r = w.Children.toArray(t.children)[0],
                  o = r.props || {},
                  a = Array.isArray(o.domain)
                    ? o.domain
                    : o.domain && o.domain[e];
                if (!o.children && a) return a;
                var i = n([r]);
                return 0 === i.length ? [0, 1] : [It.ao(i), It.MN(i)];
              },
            },
            {
              key: "pickProps",
              value: function () {
                return (
                  (this.state &&
                    this.state.nodesWillExit &&
                    this.state.oldProps) ||
                  this.props
                );
              },
            },
            {
              key: "pickDomainProps",
              value: function (t) {
                var e,
                  n =
                    null === (e = t.animate) || void 0 === e
                      ? void 0
                      : e.parentState;
                return n && n.nodesWillExit
                  ? ((this.continuous || n.continuous) &&
                      (n.nextProps || this.state.nextProps)) ||
                      t
                  : (this.continuous &&
                      this.state.nodesWillExit &&
                      this.state.nextProps) ||
                      t;
              },
            },
            {
              key: "getClipWidth",
              value: function (t, e) {
                var n = this.transitionProps
                  ? this.transitionProps.clipWidth
                  : void 0;
                return void 0 !== n
                  ? n
                  : (function () {
                      var n = Rt.rx(e.props, "x");
                      return n ? Math.abs(n[1] - n[0]) : t.width;
                    })();
              },
            },
            {
              key: "render",
              value: function () {
                var t,
                  e = this,
                  n = this.pickProps(),
                  r =
                    null !== (t = this.props.animate) &&
                    void 0 !== t &&
                    t.getTransitions
                      ? this.props.animate.getTransitions
                      : Nt.C(n, this.state, function (t) {
                          return e.setState(t);
                        }),
                  o = w.Children.toArray(n.children)[0],
                  a = r(o);
                this.transitionProps = a;
                var i = {
                    x: this.getDomainFromChildren(this.pickDomainProps(n), "x"),
                    y: this.getDomainFromChildren(n, "y"),
                  },
                  l = this.getClipWidth(n, o),
                  u = b()({ domain: i, clipWidth: l }, a, o.props),
                  s = (n.animationWhitelist || []).concat(["clipWidth"]),
                  f = s.length ? c()(u, s) : u;
                return w.createElement(
                  Dt,
                  Wt({}, u.animate, { data: f }),
                  function (t) {
                    if (o.props.groupComponent) {
                      var n = e.continuous
                        ? w.cloneElement(o.props.groupComponent, {
                            clipWidth: t.clipWidth || 0,
                          })
                        : o.props.groupComponent;
                      return w.cloneElement(
                        o,
                        b()(
                          { animate: null, animating: !0, groupComponent: n },
                          t,
                          u,
                        ),
                      );
                    }
                    return w.cloneElement(
                      o,
                      b()({ animate: null, animating: !0 }, t, u),
                    );
                  },
                );
              },
            },
          ]) && Ft(e.prototype, n),
          r && Ft(e, r),
          Object.defineProperty(e, "prototype", { writable: !1 }),
          a
        );
      })(w.Component);
      function Ht(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return Vt(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return Vt(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return Vt(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function Vt(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function $t(t, e) {
        for (var n = 0; n < e.length; n++) {
          var r = e[n];
          (r.enumerable = r.enumerable || !1),
            (r.configurable = !0),
            "value" in r && (r.writable = !0),
            Object.defineProperty(t, r.key, r);
        }
      }
      function Yt(t, e) {
        return (
          (Yt = Object.setPrototypeOf
            ? Object.setPrototypeOf.bind()
            : function (t, e) {
                return (t.__proto__ = e), t;
              }),
          Yt(t, e)
        );
      }
      function Zt(t) {
        var e = (function () {
          if ("undefined" === typeof Reflect || !Reflect.construct) return !1;
          if (Reflect.construct.sham) return !1;
          if ("function" === typeof Proxy) return !0;
          try {
            return (
              Boolean.prototype.valueOf.call(
                Reflect.construct(Boolean, [], function () {}),
              ),
              !0
            );
          } catch (t) {
            return !1;
          }
        })();
        return function () {
          var n,
            r = Gt(t);
          if (e) {
            var o = Gt(this).constructor;
            n = Reflect.construct(r, arguments, o);
          } else n = r.apply(this, arguments);
          return (function (t, e) {
            if (e && ("object" === typeof e || "function" === typeof e))
              return e;
            if (void 0 !== e)
              throw new TypeError(
                "Derived constructors may only return object or undefined",
              );
            return Kt(t);
          })(this, n);
        };
      }
      function Kt(t) {
        if (void 0 === t)
          throw new ReferenceError(
            "this hasn't been initialised - super() hasn't been called",
          );
        return t;
      }
      function Gt(t) {
        return (
          (Gt = Object.setPrototypeOf
            ? Object.getPrototypeOf.bind()
            : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t);
              }),
          Gt(t)
        );
      }
      (qt.displayName = "VictoryTransition"),
        (qt.propTypes = {
          animate: k().oneOfType([k().bool, k().object]),
          animationWhitelist: k().array,
          children: k().node,
        }),
        (qt.contextType = kt.Z);
      var Xt = function (t) {
          return !f()(t._x) && !f()(t._y);
        },
        Qt = [
          { name: "parent", index: "parent" },
          { name: "data" },
          { name: "labels" },
        ];
      function Jt(t) {
        var e =
            arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {},
          n = (function (n) {
            !(function (t, e) {
              if ("function" !== typeof e && null !== e)
                throw new TypeError(
                  "Super expression must either be null or a function",
                );
              (t.prototype = Object.create(e && e.prototype, {
                constructor: { value: t, writable: !0, configurable: !0 },
              })),
                Object.defineProperty(t, "prototype", { writable: !1 }),
                e && Yt(t, e);
            })(s, n);
            var r,
              o,
              i,
              l = Zt(s);
            function s(t) {
              var e;
              return (
                (function (t, e) {
                  if (!(t instanceof e))
                    throw new TypeError("Cannot call a class as a function");
                })(this, s),
                ((e = l.call(this, t)).state = {}),
                (e.getEventState = C.Ki.bind(Kt(e))),
                (e.getScopedEvents = C.$V.bind(Kt(e))),
                (e.getEvents = function (t, n, r) {
                  return C.vw.call(Kt(e), t, n, r, e.getScopedEvents);
                }),
                (e.externalMutations = e.getExternalMutations(e.props)),
                (e.calculatedState = e.getStateChanges(e.props)),
                (e.globalEvents = {}),
                (e.prevGlobalEventKeys = []),
                (e.boundGlobalEvents = {}),
                e.cacheValues(e.getCalculatedValues(t)),
                e
              );
            }
            return (
              (r = s),
              (o = [
                {
                  key: "shouldComponentUpdate",
                  value: function (t) {
                    var e = this.getExternalMutations(t),
                      n = this.props.animating || this.props.animate,
                      r = !A()(e, this.externalMutations);
                    if (n || r)
                      return (
                        this.cacheValues(this.getCalculatedValues(t)),
                        (this.externalMutations = e),
                        this.applyExternalMutations(t, e),
                        !0
                      );
                    var o = this.getStateChanges(t);
                    return A()(this.calculatedState, o)
                      ? !A()(this.props, t) &&
                          (this.cacheValues(this.getCalculatedValues(t)), !0)
                      : (this.cacheValues(this.getCalculatedValues(t)), !0);
                  },
                },
                {
                  key: "componentDidMount",
                  value: function () {
                    var t = this,
                      e = u()(this.globalEvents);
                    e.forEach(function (e) {
                      return t.addGlobalListener(e);
                    }),
                      (this.prevGlobalEventKeys = e);
                  },
                },
                {
                  key: "componentDidUpdate",
                  value: function (t) {
                    var e = this,
                      n = this.getStateChanges(t);
                    this.calculatedState = n;
                    var r = u()(this.globalEvents);
                    m()(this.prevGlobalEventKeys, r).forEach(function (t) {
                      return e.removeGlobalListener(t);
                    }),
                      m()(r, this.prevGlobalEventKeys).forEach(function (t) {
                        return e.addGlobalListener(t);
                      }),
                      (this.prevGlobalEventKeys = r);
                  },
                },
                {
                  key: "componentWillUnmount",
                  value: function () {
                    var t = this;
                    this.prevGlobalEventKeys.forEach(function (e) {
                      return t.removeGlobalListener(e);
                    });
                  },
                },
                {
                  key: "addGlobalListener",
                  value: function (t) {
                    var e = this,
                      n = function (n) {
                        var r = e.globalEvents[t];
                        return r && r(C.ss(n));
                      };
                    (this.boundGlobalEvents[t] = n),
                      window.addEventListener(C.Ih(t), n);
                  },
                },
                {
                  key: "removeGlobalListener",
                  value: function (t) {
                    window.removeEventListener(
                      C.Ih(t),
                      this.boundGlobalEvents[t],
                    );
                  },
                },
                {
                  key: "getStateChanges",
                  value: function (t) {
                    var n = this;
                    if (!this.hasEvents) return {};
                    var r = function (t, e) {
                      var r = b()(
                        {},
                        n.getEventState(t, e),
                        n.getSharedEventState(t, e),
                      );
                      return v()(r) ? void 0 : r;
                    };
                    return (e.components || Qt)
                      .map(function (e) {
                        if (t.standalone || "parent" !== e.name)
                          return void 0 !== e.index
                            ? r(e.index, e.name)
                            : n.dataKeys
                                .map(function (t) {
                                  return r(t, e.name);
                                })
                                .filter(Boolean);
                      })
                      .filter(Boolean);
                  },
                },
                {
                  key: "applyExternalMutations",
                  value: function (t, e) {
                    if (!v()(e)) {
                      var n = t.externalEventMutations.reduce(function (t, e) {
                          return (t = d()(e.callback)
                            ? t.concat(e.callback)
                            : t);
                        }, []),
                        r = n.length
                          ? function () {
                              n.forEach(function (t) {
                                return t();
                              });
                            }
                          : void 0;
                      this.setState(e, r);
                    }
                  },
                },
                {
                  key: "getCalculatedValues",
                  value: function (e) {
                    var n = e.sharedEvents,
                      r = t.expectedComponents,
                      o = C.pA(e, r),
                      a =
                        n && d()(n.getEventState)
                          ? n.getEventState
                          : function () {},
                      i = this.getBaseProps(e, a);
                    return {
                      componentEvents: o,
                      getSharedEventState: a,
                      baseProps: i,
                      dataKeys: u()(i).filter(function (t) {
                        return "parent" !== t;
                      }),
                      hasEvents: e.events || e.sharedEvents || o,
                      events: this.getAllEvents(e),
                    };
                  },
                },
                {
                  key: "getExternalMutations",
                  value: function (t) {
                    var e = t.sharedEvents,
                      n = t.externalEventMutations;
                    return v()(n) || e
                      ? void 0
                      : C.g2(n, this.baseProps, this.state);
                  },
                },
                {
                  key: "cacheValues",
                  value: function (t) {
                    var e = this;
                    u()(t).forEach(function (n) {
                      e[n] = t[n];
                    });
                  },
                },
                {
                  key: "getBaseProps",
                  value: function (e, n) {
                    var r = (n = n || this.getSharedEventState.bind(this))(
                        "parent",
                        "parent",
                      ),
                      o = this.getEventState("parent", "parent"),
                      a = b()({}, o, r),
                      i = a.parentControlledProps,
                      l = i ? c()(a, i) : {},
                      u = b()({}, l, e);
                    return "function" === typeof t.getBaseProps
                      ? t.getBaseProps(u)
                      : {};
                  },
                },
                {
                  key: "getAllEvents",
                  value: function (t) {
                    var e;
                    return Array.isArray(this.componentEvents)
                      ? Array.isArray(t.events)
                        ? (e = this.componentEvents).concat.apply(
                            e,
                            Ht(t.events),
                          )
                        : this.componentEvents
                      : t.events;
                  },
                },
                {
                  key: "getComponentProps",
                  value: function (e, n, r) {
                    var o = this.props.name || t.role,
                      a = (this.dataKeys && this.dataKeys[r]) || r,
                      i = "".concat(o, "-").concat(n, "-").concat(a),
                      c =
                        (this.baseProps[a] && this.baseProps[a][n]) ||
                        this.baseProps[a];
                    if (c || this.hasEvents) {
                      if (this.hasEvents) {
                        var l = this.getEvents(this.props, n, a),
                          u = b()(
                            { index: r, key: i },
                            this.getEventState(a, n),
                            this.getSharedEventState(a, n),
                            e.props,
                            c,
                            { id: i },
                          ),
                          s = b()({}, C.Z8(l, a, u), u.events);
                        return O()({}, u, { events: s });
                      }
                      return b()({ index: r, key: i }, e.props, c, { id: i });
                    }
                  },
                },
                {
                  key: "renderContainer",
                  value: function (t, e) {
                    var n =
                      t.type && "container" === t.type.role
                        ? this.getComponentProps(t, "parent", "parent")
                        : {};
                    return (
                      n.events &&
                        ((this.globalEvents = C.hy(n.events)),
                        (n.events = C.fM(n.events))),
                      w.cloneElement(t, n, e)
                    );
                  },
                },
                {
                  key: "animateComponent",
                  value: function (t, e) {
                    var n,
                      r =
                        ("object" === typeof t.animate &&
                          (null === (n = t.animate) || void 0 === n
                            ? void 0
                            : n.animationWhitelist)) ||
                        e,
                      o = this.constructor;
                    return w.createElement(
                      qt,
                      { animate: t.animate, animationWhitelist: r },
                      w.createElement(o, t),
                    );
                  },
                },
                {
                  key: "renderContinuousData",
                  value: function (t) {
                    var e = this,
                      n = t.dataComponent,
                      r = t.labelComponent,
                      o = t.groupComponent,
                      i = a()(this.dataKeys, "all").reduce(function (t, n) {
                        var o = e.getComponentProps(r, "labels", n);
                        return (
                          o &&
                            void 0 !== o.text &&
                            null !== o.text &&
                            (t = t.concat(w.cloneElement(r, o))),
                          t
                        );
                      }, []),
                      c = this.getComponentProps(n, "data", "all"),
                      l = [w.cloneElement(n, c)].concat(Ht(i));
                    return this.renderContainer(o, l);
                  },
                },
                {
                  key: "renderData",
                  value: function (t) {
                    var e = this,
                      n =
                        arguments.length > 1 && void 0 !== arguments[1]
                          ? arguments[1]
                          : Xt,
                      r = t.dataComponent,
                      o = t.labelComponent,
                      a = t.groupComponent,
                      i = this.dataKeys.reduce(function (t, o, a) {
                        var i = e.getComponentProps(r, "data", a);
                        return n(i.datum) && t.push(w.cloneElement(r, i)), t;
                      }, []),
                      c = this.dataKeys
                        .map(function (t, n) {
                          var r = e.getComponentProps(o, "labels", n);
                          if (void 0 !== r.text && null !== r.text)
                            return w.cloneElement(o, r);
                        })
                        .filter(Boolean),
                      l = [].concat(Ht(i), Ht(c));
                    return this.renderContainer(a, l);
                  },
                },
              ]),
              o && $t(r.prototype, o),
              i && $t(r, i),
              Object.defineProperty(r, "prototype", { writable: !1 }),
              s
            );
          })(t);
        return n;
      }
    },
    4463: (t, e, n) => {
      "use strict";
      n.d(e, {
        Js: () => B,
        OO: () => I,
        P$: () => N,
        TY: () => Z,
        X$: () => R,
        cp: () => F,
        dd: () => L,
        eE: () => W,
        fj: () => H,
        ge: () => $,
        kM: () => z,
        qM: () => D,
        w5: () => Y,
      });
      var r = n(41761),
        o = n.n(r),
        a = n(40806),
        i = n.n(a),
        c = n(92063),
        l = n.n(c),
        u = n(45812),
        s = n.n(u),
        f = n(66222),
        p = n.n(f),
        d = n(72064),
        h = n.n(d),
        v = n(65417),
        y = n.n(v),
        m = n(8092),
        g = n.n(m),
        b = n(74786),
        x = n.n(b),
        O = n(2100),
        w = n.n(O),
        C = n(66933),
        S = n.n(C),
        A = n(15687),
        j = n.n(A),
        k = n(72791),
        P = n(15896),
        E = n(28275),
        M = n(8091);
      function T(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return _(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return _(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return _(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function _(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function L(t) {
        return t.dependentAxis ? "y" : "x";
      }
      function D(t, e) {
        e = e || w();
        var n = function (t) {
          return t.reduce(function (t, r) {
            return r.type && "axis" === r.type.role && e(r)
              ? t.concat(r)
              : r.props && r.props.children
                ? t.concat(n(k.Children.toArray(r.props.children)))
                : t;
          }, []);
        };
        return n(t);
      }
      function I(t, e) {
        return D(t, function (t) {
          return t.type.getAxis(t.props) === e;
        })[0];
      }
      function R(t, e) {
        var n = function (t) {
          return t.reduce(function (t, r) {
            return (r.type &&
              "axis" === r.type.role &&
              (function (t) {
                return "dependent" === e
                  ? t.props.dependentAxis
                  : !t.props.dependentAxis;
              })(r)) ||
              (r.props &&
                r.props.children &&
                n(k.Children.toArray(r.props.children)).length > 0)
              ? t.concat(r)
              : t;
          }, []);
        };
        return n(t);
      }
      function N(t) {
        var e = function (t) {
          var e = Math.min.apply(Math, T(t)),
            n = Math.max.apply(Math, T(t));
          return n < 0 ? n : Math.max(0, e);
        };
        return {
          x: P.AM(t.x) ? new Date(Math.min.apply(Math, T(t.x))) : e(t.x),
          y: P.AM(t.y) ? new Date(Math.min.apply(Math, T(t.y))) : e(t.y),
        };
      }
      function W(t, e) {
        return P.AM(e)
          ? "positive"
          : t <= 0 && Math.max.apply(Math, T(e)) <= 0
            ? "negative"
            : "positive";
      }
      function F(t) {
        return { top: !1, bottom: !1, left: !0, right: !0 }[
          t.orientation || (t.dependentAxis ? "left" : "bottom")
        ];
      }
      function z(t) {
        return void 0 !== t.tickValues && P.kL(t.tickValues);
      }
      function U(t) {
        var e = t.tickValues,
          n = t.tickFormat;
        if (0 === (null === e || void 0 === e ? void 0 : e.length)) return [];
        var r = L(t),
          o = t.stringMap && t.stringMap[r],
          a = e;
        o &&
          (a = (function (t) {
            var e = L(t),
              n = t.stringMap && t.stringMap[e],
              r = Array.isArray(t.categories)
                ? t.categories
                : t.categories && t.categories[e],
              o =
                r && P.bO(r)
                  ? r.map(function (t) {
                      return n[t];
                    })
                  : void 0,
              a = n && l()(n);
            return o && 0 !== o.length ? o : a;
          })(t)),
          e &&
            P.kL(e) &&
            (a = o
              ? e.map(function (t) {
                  return o[t];
                })
              : p()(1, e.length + 1));
        var i = a
          ? h()(a)
          : (function () {
              if (n && Array.isArray(n))
                return P.kL(n)
                  ? n.map(function (t, e) {
                      return e;
                    })
                  : n;
            })();
        return Array.isArray(i) && i.length
          ? (function (e) {
              var n = [],
                o = (t.domain && t.domain[r]) || t.domain;
              if (e)
                return (
                  e.forEach(function (t, e) {
                    Array.isArray(o)
                      ? t >= P.ao(o) &&
                        t <= P.MN(o) &&
                        n.push({ value: t, index: e })
                      : n.push({ value: t, index: e });
                  }),
                  n
                );
            })(i)
          : void 0;
      }
      function B(t, e) {
        var n = t.tickFormat,
          r = L(t),
          o = t.stringMap && t.stringMap[r];
        if (!n) {
          var a = (function (t) {
              var e = t.tickValues,
                n = L(t),
                r = t.stringMap && t.stringMap[n],
                o =
                  e && !P.AM(e)
                    ? function (t) {
                        return t;
                      }
                    : void 0;
              if (!r)
                return z(t)
                  ? function (t, n) {
                      return e[n];
                    }
                  : o;
              var a = r && y()(r),
                i = s()(l()(r), function (t) {
                  return t;
                }).map(function (t) {
                  return a[t];
                }),
                c = [""].concat(T(i), [""]);
              return function (t) {
                return c[t];
              };
            })(t),
            i =
              e.tickFormat && x()(e.tickFormat)
                ? e.tickFormat()
                : function (t) {
                    return t;
                  };
          return a || i;
        }
        if (n && Array.isArray(n)) {
          var c = U(t),
            u =
              null === c || void 0 === c
                ? void 0
                : c.map(function (t) {
                    return t.index;
                  }),
            f = n.filter(function (t, e) {
              return null === u || void 0 === u ? void 0 : u.includes(e);
            });
          return function (t, e) {
            return f[e];
          };
        }
        if (n && x()(n)) {
          return o
            ? function (e, n, r) {
                var a = y()(o),
                  i = r.map(function (t) {
                    return a[t];
                  });
                return t.tickFormat(a[e], n, i);
              }
            : n;
        }
        return function (t) {
          return t;
        };
      }
      function q(t, e) {
        if (!e || !Array.isArray(t) || t.length <= e) return t;
        var n = Math.floor(t.length / e);
        return t.filter(function (t, e) {
          return e % n === 0;
        });
      }
      function H(t, e) {
        var n = arguments.length > 2 && void 0 !== arguments[2] && arguments[2],
          r = t.tickCount,
          a = U(t);
        if (0 === (null === a || void 0 === a ? void 0 : a.length)) return [""];
        var c = a
          ? a.map(function (t) {
              return t.value;
            })
          : void 0;
        if (c) return q(c, r);
        if (e.ticks && x()(e.ticks)) {
          var l = r || 5,
            u = e.ticks(l),
            s = q(Array.isArray(u) && u.length ? u : e.domain(), r);
          if (n) {
            var f = i()(s, 0) ? o()(s, 0) : s;
            return f.length ? f : s;
          }
          return s;
        }
        return e.domain();
      }
      function V(t, e) {
        var n = t.polar,
          r = t.startAngle,
          o = void 0 === r ? 0 : r,
          a = t.endAngle,
          i = void 0 === a ? 360 : a,
          c = U(t),
          l =
            c && 0 !== (null === c || void 0 === c ? void 0 : c.length)
              ? c.map(function (t) {
                  return t.value;
                })
              : void 0;
        if (Array.isArray(l)) {
          var u = E.bZ(t, e),
            s = E.lg(t, e),
            f = z(t),
            p = l.map(function (t) {
              return Number(t);
            }),
            d = f ? 1 : P.ao(p),
            h = f ? l.length : P.MN(p),
            v = void 0 !== u ? u : d,
            y = void 0 !== s ? s : h,
            m = E.CU(v, y),
            g = n && "x" === e && 360 === Math.abs(o - i) ? E.eV(m, p) : m;
          return F(t) && !n && g.reverse(), g;
        }
      }
      function $(t, e) {
        var n = L(t);
        if (!e || e === n) return E.Ae(V)(t, n);
      }
      function Y(t, e) {
        if (t.axisValue) {
          var n = "x" === e ? "y" : "x",
            r = g()(t.scale) && x()(t.scale[n]) ? t.scale[n] : void 0;
          if (r) {
            var o = "x" === e ? "y" : "x",
              a = g()(t.stringMap) && t.stringMap[o];
            return r(
              a && "string" === typeof t.axisValue
                ? a[t.axisValue]
                : t.axisValue,
            );
          }
        }
      }
      function Z(t, e) {
        if (!g()(t.theme)) return M.TY(t, e, "axis");
        var n = "axis";
        if (
          (t.dependentAxis && t.theme.dependentAxis
            ? (n = "dependentAxis")
            : !t.dependentAxis &&
              t.theme.independentAxis &&
              (n = "independentAxis"),
          "axis" === n)
        )
          return M.TY(t, e, "axis");
        var r = S()({}, t.theme[n], t.theme.axis),
          o = j()({}, t.theme, { axis: r });
        return M.TY(j()({}, t, { theme: o }), e, "axis");
      }
    },
    15896: (t, e, n) => {
      "use strict";
      function r(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return o(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return o(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return o(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function o(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function a(t) {
        return Array.isArray(t) && t.length > 0;
      }
      function i(t) {
        return (
          Array.isArray(t) &&
          t.some(function (t) {
            return "string" === typeof t;
          })
        );
      }
      function c(t) {
        return (
          Array.isArray(t) &&
          t.some(function (t) {
            return t instanceof Date;
          })
        );
      }
      function l(t) {
        return (
          a(t) &&
          t.every(function (t) {
            return "string" === typeof t;
          })
        );
      }
      function u(t) {
        return a(t) && t.every(Array.isArray);
      }
      function s(t) {
        return t.filter(function (t) {
          return void 0 !== t;
        });
      }
      function f(t) {
        for (
          var e = arguments.length, n = new Array(e > 1 ? e - 1 : 0), o = 1;
          o < e;
          o++
        )
          n[o - 1] = arguments[o];
        var a = t.concat(n);
        return c(a)
          ? new Date(Math.max.apply(Math, r(a)))
          : Math.max.apply(Math, r(a));
      }
      function p(t) {
        for (
          var e = arguments.length, n = new Array(e > 1 ? e - 1 : 0), o = 1;
          o < e;
          o++
        )
          n[o - 1] = arguments[o];
        var a = t.concat(n);
        return c(a)
          ? new Date(Math.min.apply(Math, r(a)))
          : Math.min.apply(Math, r(a));
      }
      n.d(e, {
        AM: () => c,
        Jr: () => u,
        MN: () => f,
        ao: () => p,
        bO: () => l,
        kL: () => i,
        o2: () => s,
      });
    },
    46577: (t, e, n) => {
      "use strict";
      n.d(e, { l: () => i });
      var r = n(52007),
        o = n.n(r),
        a = n(42745),
        i = {
          dataProps: {
            categories: o().oneOfType([
              o().arrayOf(o().string),
              o().shape({
                x: o().arrayOf(o().string),
                y: o().arrayOf(o().string),
              }),
            ]),
            data: o().oneOfType([o().array, o().object]),
            dataComponent: o().element,
            disableInlineStyles: o().bool,
            labelComponent: o().element,
            labels: o().oneOfType([o().func, o().array]),
            samples: a.A7,
            sortKey: o().oneOfType([
              o().func,
              a.BO([a._L, a.A7]),
              o().string,
              o().arrayOf(o().string.isRequired),
            ]),
            sortOrder: o().oneOf(["ascending", "descending"]),
            style: o().shape({
              parent: o().object,
              data: o().object,
              labels: o().object,
            }),
            x: o().oneOfType([
              o().func,
              a.BO([a._L, a.A7]),
              o().string,
              o().arrayOf(o().string.isRequired),
            ]),
            y: o().oneOfType([
              o().func,
              a.BO([a._L, a.A7]),
              o().string,
              o().arrayOf(o().string.isRequired),
            ]),
            y0: o().oneOfType([
              o().func,
              a.BO([a._L, a.A7]),
              o().string,
              o().arrayOf(o().string.isRequired),
            ]),
          },
          baseProps: {
            animate: o().oneOfType([o().bool, o().object]),
            containerComponent: o().element,
            domain: o().oneOfType([a.nw, o().shape({ x: a.nw, y: a.nw })]),
            maxDomain: o().oneOfType([
              o().number,
              o().instanceOf(Date),
              o().shape({
                x: o().oneOfType([o().number, o().instanceOf(Date)]),
                y: o().oneOfType([o().number, o().instanceOf(Date)]),
              }),
            ]),
            minDomain: o().oneOfType([
              o().number,
              o().instanceOf(Date),
              o().shape({
                x: o().oneOfType([o().number, o().instanceOf(Date)]),
                y: o().oneOfType([o().number, o().instanceOf(Date)]),
              }),
            ]),
            domainPadding: o().oneOfType([
              o().shape({
                x: o().oneOfType([o().number, o().arrayOf(o().number)]),
                y: o().oneOfType([o().number, o().arrayOf(o().number)]),
              }),
              o().number,
              o().arrayOf(o().number),
            ]),
            eventKey: o().oneOfType([o().func, a.BO([a._L, a.A7]), o().string]),
            events: o().arrayOf(
              o().shape({
                target: o().oneOf(["data", "labels", "parent"]),
                eventKey: o().oneOfType([
                  o().array,
                  a.BO([a._L, a.A7]),
                  o().string,
                ]),
                eventHandlers: o().object,
              }),
            ),
            externalEventMutations: o().arrayOf(
              o().shape({
                callback: o().func,
                childName: o().oneOfType([o().string, o().array]),
                eventKey: o().oneOfType([
                  o().array,
                  a.BO([a._L, a.A7]),
                  o().string,
                ]),
                mutation: o().func,
                target: o().oneOfType([o().string, o().array]),
              }),
            ),
            groupComponent: o().element,
            height: a.A7,
            name: o().string,
            origin: o().shape({ x: o().number, y: o().number }),
            padding: o().oneOfType([
              o().number,
              o().shape({
                top: o().number,
                bottom: o().number,
                left: o().number,
                right: o().number,
              }),
            ]),
            polar: o().bool,
            range: o().oneOfType([
              a.nw,
              o().shape({ x: a.nw.isRequired, y: a.nw.isRequired }),
            ]),
            scale: o().oneOfType([
              a.bA,
              o().shape({ x: a.bA.isRequired, y: a.bA.isRequired }),
            ]),
            sharedEvents: o().shape({
              events: o().array,
              getEventState: o().func,
            }),
            singleQuadrantDomainPadding: o().oneOfType([
              o().bool,
              o().shape({
                x: o().oneOfType([o().bool]),
                y: o().oneOfType([o().bool]),
              }),
            ]),
            standalone: o().bool,
            theme: o().object,
            width: a.A7,
          },
          primitiveProps: {
            active: o().bool,
            ariaLabel: o().oneOfType([o().string, o().func]),
            className: o().string,
            clipPath: o().string,
            data: o().oneOfType([o().array, o().object]),
            desc: o().oneOfType([o().string, o().func]),
            disableInlineStyles: o().bool,
            events: o().object,
            id: o().oneOfType([o().number, o().string, o().func]),
            index: o().oneOfType([o().number, o().string]),
            origin: o().shape({ x: o().number, y: o().number }),
            polar: o().bool,
            role: o().string,
            scale: o().oneOfType([a.bA, o().shape({ x: a.bA, y: a.bA })]),
            shapeRendering: o().string,
            style: o().object,
            tabIndex: o().oneOfType([o().number, o().func]),
            transform: o().string,
          },
        };
    },
    54481: (t, e, n) => {
      "use strict";
      n.d(e, {
        kQ: () => Y,
        CP: () => G,
        Yu: () => X,
        RU: () => Q,
        ZY: () => J,
        hi: () => tt,
      });
      var r = n(64417),
        o = n.n(r),
        a = n(42530),
        i = n.n(a),
        c = n(40806),
        l = n.n(c),
        u = n(18111),
        s = n.n(u),
        f = n(66364),
        p = n.n(f),
        d = n(45812),
        h = n.n(d),
        v = n(10038),
        y = n.n(v),
        m = n(93977),
        g = n.n(m),
        b = n(74786),
        x = n.n(b),
        O = n(15727),
        w = n.n(O),
        C = n(66222),
        S = n.n(C),
        A = n(72064),
        j = n.n(A),
        k = n(15687),
        P = n.n(k),
        E = n(72791),
        M = n(8091),
        T = n(15896),
        _ = n(20933),
        L = "@@__IMMUTABLE_ITERABLE__@@",
        D = "@@__IMMUTABLE_RECORD__@@",
        I = "@@__IMMUTABLE_LIST__@@";
      function R(t) {
        return !(!t || !t[L]);
      }
      function N(t) {
        return (
          R(t) ||
          (function (t) {
            return !(!t || !t[D]);
          })(t)
        );
      }
      function W(t, e) {
        return R(t)
          ? t.reduce(
              function (t, n, r) {
                return e && e[r] && (n = W(n)), (t[r] = n), t;
              },
              (function (t) {
                return !(!t || !t[I]);
              })(t)
                ? []
                : {},
            )
          : t;
      }
      function F(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return z(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return z(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return z(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function z(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function U(t) {
        return N(t) ? W(t, { errorX: !0, errorY: !0 }) : t;
      }
      function B(t) {
        return R(t) ? t.size : t.length;
      }
      function q(t, e) {
        var n = (g()(t.domain) ? t.domain[e] : t.domain) || _.q8(t, e).domain(),
          r = t.samples || 1,
          o = Math.max.apply(Math, F(n)),
          a = Math.min.apply(Math, F(n)),
          i = (o - a) / r,
          c = S()(a, o, i);
        return w()(c) === o ? c : c.concat(o);
      }
      function H(t, e) {
        var n =
          arguments.length > 2 && void 0 !== arguments[2]
            ? arguments[2]
            : "ascending";
        if (!e) return t;
        ("x" !== e && "y" !== e) || (e = "_".concat(e));
        var r = "ascending" === n ? "asc" : "desc";
        return h()(t, e, r);
      }
      function V(t, e) {
        var n = 1 / Number.MAX_SAFE_INTEGER,
          r = { x: _.md(e, "x"), y: _.md(e, "y") };
        if ("log" !== r.x && "log" !== r.y) return t;
        var o = function (t, e) {
          return "log" !== r[e] || 0 !== t["_".concat(e)];
        };
        return t.map(function (t) {
          return o(t, "x") && o(t, "y") && o(t, "y0")
            ? t
            : (function (t) {
                var e = o(t, "x") ? t._x : n,
                  r = o(t, "y") ? t._y : n,
                  a = o(t, "y0") ? t._y0 : n;
                return P()({}, t, { _x: e, _y: r, _y0: a });
              })(t);
        });
      }
      function $(t, e) {
        var n,
          r = !!t.eventKey,
          o =
            ((n = t.eventKey),
            x()(n) ? n : null === n || void 0 === n ? function () {} : y()(n));
        return e.map(function (t, e) {
          if (void 0 !== t.eventKey) return t;
          if (r) {
            var n = o(t, e);
            return void 0 !== n ? P()({ eventKey: n }, t) : t;
          }
          return t;
        });
      }
      function Y(t, e, n) {
        var r = function (t) {
            return void 0 !== t;
          },
          a = T.ao(e.x),
          c = T.MN(e.x),
          l = T.ao(e.y),
          u = T.MN(e.y),
          s = function (t) {
            return function (e) {
              return r(e) && e < t;
            };
          },
          f = function (t) {
            return function (e) {
              return r(e) && e > t;
            };
          },
          p = s(a),
          d = s(l),
          h = f(c),
          v = f(u);
        return t.map(function (t) {
          var e = t._x,
            a = t._y,
            c = t._y0,
            s = t._y1;
          (p(e) || h(e)) && (e = null);
          var f = r(c) ? c : n,
            y = r(s) ? s : a;
          return r(y)
            ? (r(f) || (!d(y) && !v(y)) || (a = null),
              ((d(f) && d(y)) || (v(f) && v(y))) && (a = c = s = null),
              d(f) && !d(y) && (c = l),
              v(f) && !v(y) && (c = u),
              P()({}, t, o()({ _x: e, _y: a, _y0: c, _y1: s }, i())))
            : t;
        });
      }
      function Z(t, e) {
        var n = Q(t, e),
          r = J(t, e),
          o = (function (t, e) {
            var n = Array.isArray(t.data) || R(t.data);
            if (!n) return [];
            var r = void 0 === t[e] ? e : t[e],
              o = M.$0(r),
              a = t.data.reduce(function (t, e) {
                return t.push(U(e)), t;
              }, []),
              i = H(a, t.sortKey, t.sortOrder);
            return i
              .reduce(function (t, e) {
                return (e = U(e)), t.push(o(e)), t;
              }, [])
              .filter(function (t) {
                return "string" === typeof t;
              })
              .reduce(function (t, e) {
                return (
                  void 0 !== e &&
                    null !== e &&
                    -1 === t.indexOf(e) &&
                    t.push(e),
                  t
                );
              }, []);
          })(t, e),
          a = j()([].concat(F(n), F(r), F(o)));
        return 0 === a.length
          ? null
          : a.reduce(function (t, e, n) {
              return (t[e] = n + 1), t;
            }, {});
      }
      function K(t, e, n) {
        if (!(Array.isArray(t) || R(t)) || B(t) < 1) return [];
        var r = ["x", "y", "y0"];
        n = Array.isArray(n) ? n : r;
        var o,
          a = n.reduce(function (t, n) {
            var r;
            return (t[n] = ((r = n), M.$0(void 0 !== e[r] ? e[r] : r))), t;
          }, {}),
          i = s()(n, r) && "_x" === e.x && "_y" === e.y && "_y0" === e.y0;
        !1 === i &&
          (o = {
            x: -1 !== n.indexOf("x") ? Z(e, "x") : void 0,
            y: -1 !== n.indexOf("y") ? Z(e, "y") : void 0,
            y0: -1 !== n.indexOf("y0") ? Z(e, "y") : void 0,
          });
        var c = V(
          H(
            i
              ? t
              : t.reduce(function (t, e, r) {
                  var i = { x: r, y: (e = U(e)) },
                    c = n.reduce(function (t, n) {
                      var r = a[n](e),
                        c = void 0 !== r ? r : i[n];
                      return (
                        void 0 !== c &&
                          ("string" === typeof c && o[n]
                            ? ((t["".concat(n, "Name")] = c),
                              (t["_".concat(n)] = o[n][c]))
                            : (t["_".concat(n)] = c)),
                        t
                      );
                    }, {}),
                    l = P()({}, c, e);
                  return p()(l) || t.push(l), t;
                }, []),
            e.sortKey,
            e.sortOrder,
          ),
          e,
        );
        return $(e, c);
      }
      function G(t, e) {
        return t.categories && !Array.isArray(t.categories)
          ? t.categories[e]
          : t.categories;
      }
      function X(t) {
        return t.data
          ? K(t.data, t)
          : K(
              (function (t) {
                var e = q(t, "x"),
                  n = q(t, "y");
                return e.map(function (t, e) {
                  return { x: t, y: n[e] };
                });
              })(t),
              t,
            );
      }
      function Q(t, e) {
        var n = t.tickValues,
          r = t.tickFormat;
        return (
          n && (Array.isArray(n) || n[e])
            ? n[e] || n
            : r && Array.isArray(r)
              ? r
              : []
        ).filter(function (t) {
          return "string" === typeof t;
        });
      }
      function J(t, e) {
        if (!t.categories) return [];
        var n = G(t, e),
          r =
            n &&
            n.filter(function (t) {
              return "string" === typeof t;
            });
        return r ? T.o2(r) : [];
      }
      function tt(t) {
        var e = function (t) {
            return t && t.type ? t.type.role : "";
          },
          n = e(t);
        if ("portal" === n) {
          var r = E.Children.toArray(t.props.children);
          n = r.length ? e(r[0]) : "";
        }
        return l()(
          [
            "area",
            "bar",
            "boxplot",
            "candlestick",
            "errorbar",
            "group",
            "histogram",
            "line",
            "pie",
            "scatter",
            "stack",
            "voronoi",
          ],
          n,
        );
      }
    },
    28275: (t, e, n) => {
      "use strict";
      n.d(e, {
        $B: () => k,
        Ae: () => S,
        CU: () => P,
        Rm: () => A,
        bZ: () => _,
        eV: () => L,
        ge: () => j,
        h9: () => D,
        lP: () => E,
        lg: () => T,
        x1: () => M,
      });
      var r = n(36609),
        o = n.n(r),
        a = n(40806),
        i = n.n(a),
        c = n(74786),
        l = n.n(c),
        u = n(21139),
        s = n.n(u),
        f = n(93977),
        p = n.n(f),
        d = n(25506),
        h = n.n(d),
        v = n(72791),
        y = n(54481),
        m = n(20933),
        g = n(8091),
        b = n(15896);
      function x(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return O(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return O(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return O(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function O(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function w(t, e) {
        var n =
            arguments.length > 2 && void 0 !== arguments[2]
              ? arguments[2]
              : "min",
          r = function (t) {
            return "max" === n
              ? Math.max.apply(Math, x(t))
              : Math.min.apply(Math, x(t));
          },
          o = "max" === n ? -1 / 0 : 1 / 0,
          a = !1,
          i = h()(t).reduce(function (t, n) {
            var o =
                void 0 !== n["_".concat(e, "0")]
                  ? n["_".concat(e, "0")]
                  : n["_".concat(e)],
              i =
                void 0 !== n["_".concat(e, "1")]
                  ? n["_".concat(e, "1")]
                  : n["_".concat(e)],
              c = r([o, i]);
            return (a = a || o instanceof Date || i instanceof Date), r([t, c]);
          }, o);
        return a ? new Date(i) : i;
      }
      function C(t, e, n) {
        if (!e.domainPadding) return t;
        var r = _(e, n),
          o = T(e, n),
          a = (function (t, e) {
            var n = function (t) {
              return Array.isArray(t)
                ? { left: t[0], right: t[1] }
                : { left: t, right: t };
            };
            return p()(t.domainPadding)
              ? n(t.domainPadding[e])
              : n(t.domainPadding);
          })(e, n);
        if (!a.left && !a.right) return t;
        var i = b.ao(t),
          c = b.MN(t),
          l = g.Uk(n, e.horizontal),
          u = g.rx(e, l),
          s = Math.abs(u[0] - u[1]),
          f = Math.max(s - a.left - a.right, 1),
          d = (Math.abs(c.valueOf() - i.valueOf()) / f) * s,
          h = (d * a.left) / s,
          v = (d * a.right) / s,
          y = { min: i.valueOf() - h, max: c.valueOf() + v },
          m = p()(e.singleQuadrantDomainPadding)
            ? e.singleQuadrantDomainPadding[n]
            : e.singleQuadrantDomainPadding,
          x = function (t, e) {
            return ("min" === e && i >= 0 && t <= 0) ||
              ("max" === e && c <= 0 && t >= 0)
              ? 0
              : t;
          };
        if (((i >= 0 && y.min <= 0) || (c <= 0 && y.max >= 0)) && !1 !== m) {
          var O = {
              left: (Math.abs(c - i) * a.left) / s,
              right: (Math.abs(c - i) * a.right) / s,
            },
            w = {
              min: x(i.valueOf() - O.left, "min"),
              max: x(c.valueOf() + O.right, "max"),
            },
            C = {
              left: (Math.abs(w.max - w.min) * a.left) / s,
              right: (Math.abs(w.max - w.min) * a.right) / s,
            };
          y = {
            min: x(i.valueOf() - C.left, "min"),
            max: x(c.valueOf() + C.right, "max"),
          };
        }
        var S = {
          min: void 0 !== r ? r : y.min,
          max: void 0 !== o ? o : y.max,
        };
        return i instanceof Date || c instanceof Date
          ? P(new Date(S.min), new Date(S.max))
          : P(S.min, S.max);
      }
      function S(t, e) {
        return (
          (t = l()(t) ? t : k),
          (e = l()(e) ? e : A),
          function (n, r) {
            var o = E(n, r);
            if (o) return e(o, n, r);
            var a = y.CP(n, r),
              i = a
                ? (function (t, e, n) {
                    n = n || y.CP(t, e);
                    var r = t.polar,
                      o = t.startAngle,
                      a = void 0 === o ? 0 : o,
                      i = t.endAngle,
                      c = void 0 === i ? 360 : i;
                    if (!n) return;
                    var l = _(t, e),
                      u = T(t, e),
                      s = b.kL(n) ? y.ZY(t, e) : [],
                      f =
                        0 === s.length
                          ? null
                          : s.reduce(function (t, e, n) {
                              return (t[e] = n + 1), t;
                            }, {}),
                      p = f
                        ? n.map(function (t) {
                            return f[t];
                          })
                        : n,
                      d = void 0 !== l ? l : b.ao(p),
                      h = void 0 !== u ? u : b.MN(p),
                      v = P(d, h);
                    return r && "x" === e && 360 === Math.abs(a - c)
                      ? L(v, p)
                      : v;
                  })(n, r, a)
                : t(n, r);
            return i ? e(i, n, r) : void 0;
          }
        );
      }
      function A(t, e, n) {
        return (function (t, e, n) {
          return "log" !== m.md(e, n)
            ? t
            : (function (t) {
                var e =
                  t[0] < 0 || t[1] < 0
                    ? -1 / Number.MAX_SAFE_INTEGER
                    : 1 / Number.MAX_SAFE_INTEGER;
                return [0 === t[0] ? e : t[0], 0 === t[1] ? e : t[1]];
              })(t);
        })(C(t, e, n), e, n);
      }
      function j(t, e) {
        return S()(t, e);
      }
      function k(t, e, n) {
        n = n || y.Yu(t);
        var r = t.polar,
          o = t.startAngle,
          a = void 0 === o ? 0 : o,
          i = t.endAngle,
          c = void 0 === i ? 360 : i,
          l = _(t, e),
          u = T(t, e);
        if (n.length < 1)
          return void 0 !== l && void 0 !== u ? P(l, u) : void 0;
        var s = P(
          void 0 !== l ? l : w(n, e, "min"),
          void 0 !== u ? u : w(n, e, "max"),
        );
        return r && "x" === e && 360 === Math.abs(a - c)
          ? L(
              s,
              (function (t, e) {
                var n = "_".concat(e);
                return h()(t).map(function (t) {
                  return t[n] && void 0 !== t[n][1] ? t[n][1] : t[n];
                });
              })(n, e),
            )
          : s;
      }
      function P(t, e) {
        return Number(t) === Number(e)
          ? (function (t) {
              var e = 0 === t ? 2 * Math.pow(10, -10) : Math.pow(10, -10),
                n = t instanceof Date ? new Date(Number(t) - 1) : Number(t) - e,
                r = t instanceof Date ? new Date(Number(t) + 1) : Number(t) + e;
              return 0 === t ? [0, r] : [n, r];
            })(e)
          : [t, e];
      }
      function E(t, e) {
        var n = _(t, e),
          r = T(t, e);
        return p()(t.domain) && t.domain[e]
          ? t.domain[e]
          : Array.isArray(t.domain)
            ? t.domain
            : void 0 !== n && void 0 !== r
              ? P(n, r)
              : void 0;
      }
      function M(t, e) {
        var n = E(t, e);
        if (n) return n;
        var r = y.Yu(t),
          o = r.reduce(function (t, e) {
            return e._y0 < t ? e._y0 : t;
          }, 1 / 0);
        return S(
          function () {
            return k(t, e, r);
          },
          function (n) {
            return A(
              (function (n) {
                if ("x" === e) return n;
                var r = o !== 1 / 0 ? o : 0,
                  a = T(t, e),
                  i = _(t, e),
                  c = void 0 !== a ? a : b.MN(n, r);
                return P(void 0 !== i ? i : b.ao(n, r), c);
              })(n),
              t,
              e,
            );
          },
        )(t, e);
      }
      function T(t, e) {
        return p()(t.maxDomain) && void 0 !== t.maxDomain[e]
          ? t.maxDomain[e]
          : "number" === typeof t.maxDomain || o()(t.maxDomain)
            ? t.maxDomain
            : void 0;
      }
      function _(t, e) {
        return p()(t.minDomain) && void 0 !== t.minDomain[e]
          ? t.minDomain[e]
          : "number" === typeof t.minDomain || o()(t.minDomain)
            ? t.minDomain
            : void 0;
      }
      function L(t, e) {
        var n = s()(
            e.sort(function (t, e) {
              return t - e;
            }),
          ),
          r = n[1] - n[0];
        return [t[0], t[1] + r];
      }
      function D(t) {
        var e = function (t) {
            return t && t.type ? t.type.role : "";
          },
          n = e(t);
        if ("portal" === n) {
          var r = v.Children.toArray(t.props.children);
          n = r.length ? e(r[0]) : "";
        }
        return i()(
          [
            "area",
            "axis",
            "bar",
            "boxplot",
            "candlestick",
            "errorbar",
            "group",
            "histogram",
            "line",
            "pie",
            "scatter",
            "stack",
            "voronoi",
          ],
          n,
        );
      }
    },
    79704: (t, e, n) => {
      "use strict";
      n.d(e, {
        $V: () => j,
        Ih: () => L,
        Ki: () => P,
        Z8: () => k,
        fM: () => I,
        g2: () => M,
        gX: () => E,
        hy: () => D,
        pA: () => _,
        ss: () => R,
        vw: () => A,
      });
      var r = n(12742),
        o = n.n(r),
        a = n(40806),
        i = n.n(a),
        c = n(72064),
        l = n.n(c),
        u = n(64417),
        s = n.n(u),
        f = n(87790),
        p = n.n(f),
        d = n(41761),
        h = n.n(d),
        v = n(74786),
        y = n.n(v),
        m = n(66364),
        g = n.n(m),
        b = n(15687),
        x = n.n(b);
      function O(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      function w(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return C(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return C(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return C(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function C(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      var S = /^onGlobal(.*)$/;
      function A(t, e, n, r) {
        var o = this,
          a = function (t) {
            var r = (function () {
              var r = t.reduce(function (t, n) {
                return void 0 !== n.target
                  ? (
                      Array.isArray(n.target)
                        ? i()(n.target, e)
                        : "".concat(n.target) === "".concat(e)
                    )
                    ? t.concat(n)
                    : t
                  : t.concat(n);
              }, []);
              return void 0 !== n && "parent" !== e
                ? r.filter(function (t) {
                    var e = t.eventKey,
                      r = function (t) {
                        return !t || "".concat(t) === "".concat(n);
                      };
                    return Array.isArray(e)
                      ? e.some(function (t) {
                          return r(t);
                        })
                      : r(e);
                  })
                : r;
            })();
            return (
              Array.isArray(r) &&
              r.reduce(function (t, e) {
                return e ? x()(t, e.eventHandlers) : t;
              }, {})
            );
          },
          c = (function () {
            var e;
            return Array.isArray(o.componentEvents)
              ? Array.isArray(t.events)
                ? (e = o.componentEvents).concat.apply(e, w(t.events))
                : o.componentEvents
              : t.events;
          })(),
          l = c && y()(r) ? r(a(c), e) : void 0;
        if (!t.sharedEvents) return l;
        var u = t.sharedEvents.getEvents,
          s = t.sharedEvents.events && u(a(t.sharedEvents.events), e);
        return x()({}, s, l);
      }
      function j(t, e, n, r) {
        var a = this;
        if (g()(t)) return {};
        r = r || this.baseProps;
        var i = function (t, e) {
            var n = t.childName,
              o = t.target,
              i = t.key,
              c = "props" === e ? r : a.state || {},
              l = void 0 !== n && null !== n && c[n] ? c[n] : c;
            return "parent" === i ? l.parent : l[i] && l[i][o];
          },
          c = function (t, c) {
            var l = "parent" === e ? t.childName : t.childName || n,
              u = t.target || e,
              s = function (e, n) {
                var c = a.state || {};
                if (!y()(t.mutation)) return c;
                var l = i({ childName: n, key: e, target: u }, "props"),
                  s = i({ childName: n, key: e, target: u }, "state"),
                  f = t.mutation(x()({}, l, s), r),
                  p = c[n] || {},
                  d = function (t) {
                    return f
                      ? (function (t) {
                          return "parent" === u
                            ? x()(t, O({}, e, x()(t[e], f)))
                            : x()(t, O({}, e, x()(t[e], O({}, u, f))));
                        })(t)
                      : (function (t) {
                          return (
                            t[e] && t[e][u] && delete t[e][u],
                            t[e] && !o()(t[e]).length && delete t[e],
                            t
                          );
                        })(t);
                  };
                return void 0 !== n && null !== n
                  ? x()(c, O({}, n, d(p)))
                  : d(c);
              },
              f = function (e) {
                var n = (function (e) {
                  return "parent" === u
                    ? "parent"
                    : "all" === t.eventKey
                      ? r[e]
                        ? h()(o()(r[e]), "parent")
                        : h()(o()(r), "parent")
                      : void 0 === t.eventKey && "parent" === c
                        ? r[e]
                          ? o()(r[e])
                          : o()(r)
                        : void 0 !== t.eventKey
                          ? t.eventKey
                          : c;
                })(e);
                return Array.isArray(n)
                  ? n.reduce(function (t, n) {
                      return x()(t, s(n, e));
                    }, {})
                  : s(n, e);
              },
              p = "all" === l ? h()(o()(r), "parent") : l;
            return Array.isArray(p)
              ? p.reduce(function (t, e) {
                  return x()(t, f(e));
                }, {})
              : f(p);
          },
          l = function (e, n, r, o) {
            var i = t[o](e, n, r, a);
            if (!g()(i)) {
              var l = (function (t) {
                var e = function (t) {
                    return y()(t.callback) && t.callback;
                  },
                  n = (
                    Array.isArray(t)
                      ? t.map(function (t) {
                          return e(t);
                        })
                      : [e(t)]
                  ).filter(function (t) {
                    return !1 !== t;
                  });
                return n.length
                  ? function () {
                      return n.forEach(function (t) {
                        return t();
                      });
                    }
                  : void 0;
              })(i);
              a.setState(
                (function (t, e) {
                  return Array.isArray(t)
                    ? t.reduce(function (t, n) {
                        return x()({}, t, c(n, e));
                      }, {})
                    : c(t, e);
                })(i, r),
                l,
              );
            }
          };
        return o()(t).reduce(function (t, e) {
          return (t[e] = l), t;
        }, {});
      }
      function k(t, e, n) {
        return t
          ? o()(t).reduce(function (r, o) {
              return (
                (r[o] = function (r) {
                  return t[o](r, n, e, o);
                }),
                r
              );
            }, {})
          : {};
      }
      function P(t, e, n) {
        var r = this.state || {};
        return n
          ? r[n] && r[n][t] && r[n][t][e]
          : "parent" === t
            ? (r[t] && r[t][e]) || r[t]
            : r[t] && r[t][e];
      }
      function E(t, e, n, r) {
        return (
          (e = e || {}),
          (n = n || {}),
          r.reduce(function (r, o) {
            var a = n[o],
              i = M(t, e[o], n[o], o);
            return (
              (r[o] = i || a),
              p()(r, function (t) {
                return !g()(t);
              })
            );
          }, {})
        );
      }
      function M(t, e, n, r) {
        return (
          (e = e || {}),
          (n = n || {}),
          o()(e).reduce(function (a, i) {
            var c = n[i] || {},
              u = e[i] || {};
            if ("parent" === i) {
              var s = T(t, u, c, { eventKey: i, target: "parent" });
              a[i] = void 0 !== s ? x()({}, c, s) : c;
            } else {
              var f = l()(o()(u).concat(o()(c)));
              a[i] = f.reduce(function (e, n) {
                var o = { eventKey: i, target: n, childName: r },
                  a = T(t, u[n], c[n], o);
                return (
                  (e[n] = void 0 !== a ? x()({}, c[n], a) : c[n]),
                  p()(e, function (t) {
                    return !g()(t);
                  })
                );
              }, {});
            }
            return p()(a, function (t) {
              return !g()(t);
            });
          }, {})
        );
      }
      function T(t, e, n, r) {
        var o = function (t, e) {
            if ("string" === typeof t[e])
              return "all" === t[e] || t[e] === r[e];
            if (Array.isArray(t[e])) {
              var n = t[e].map(function (t) {
                return "".concat(t);
              });
              return i()(n, r[e]);
            }
            return !1;
          },
          a = (t = Array.isArray(t) ? t : [t]);
        r.childName &&
          (a = t.filter(function (t) {
            return o(t, "childName");
          }));
        var c = a.filter(function (t) {
          return o(t, "target");
        });
        if (!g()(c)) {
          var l = c.filter(function (t) {
            return o(t, "eventKey");
          });
          if (!g()(l))
            return l.reduce(function (t, r) {
              var o = (r && y()(r.mutation) ? r.mutation : function () {})(
                x()({}, e, n),
              );
              return x()({}, t, o);
            }, {});
        }
      }
      function _(t, e) {
        var n =
          Array.isArray(e) &&
          e.reduce(function (e, n) {
            var r,
              o = t[n],
              a = o && o.type && o.type.defaultEvents,
              i = y()(a) ? a(o.props) : a;
            return (e = Array.isArray(i) ? (r = e).concat.apply(r, w(i)) : e);
          }, []);
        return n && n.length ? n : void 0;
      }
      function L(t) {
        var e = t.match(S);
        return e && e[1] && e[1].toLowerCase();
      }
      var D = function (t) {
          return p()(t, function (t, e) {
            return S.test(e);
          });
        },
        I = function (t) {
          return s()(t, function (t, e) {
            return S.test(e);
          });
        },
        R = function (t) {
          return x()(t, { nativeEvent: t });
        };
    },
    8091: (t, e, n) => {
      "use strict";
      n.d(e, {
        $0: () => M,
        CE: () => y,
        F1: () => L,
        F3: () => S,
        F8: () => m,
        H5: () => k,
        Ht: () => A,
        IW: () => P,
        Lo: () => O,
        TY: () => T,
        Uk: () => _,
        Wi: () => w,
        ij: () => x,
        q2: () => g,
        rx: () => E,
        tQ: () => b,
        vi: () => j,
        xs: () => C,
      });
      var r = n(12742),
        o = n.n(r),
        a = n(15687),
        i = n.n(a),
        c = n(36460),
        l = n.n(c),
        u = n(10038),
        s = n.n(u),
        f = n(74786),
        p = n.n(f),
        d = n(66933),
        h = n.n(d),
        v = n(72791);
      function y(t) {
        var e =
            arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : [],
          n = {};
        for (var r in t)
          e.indexOf(r) >= 0 ||
            (Object.prototype.hasOwnProperty.call(t, r) && (n[r] = t[r]));
        return n;
      }
      function m(t) {
        var e = function (t) {
            return void 0 !== t;
          },
          n = t._x,
          r = t._x1,
          o = t._x0,
          a = t._voronoiX,
          i = t._y,
          c = t._y1,
          l = t._y0,
          u = t._voronoiY,
          s = e(r) ? r : n,
          f = e(c) ? c : i,
          p = {
            x: e(a) ? a : s,
            x0: e(o) ? o : n,
            y: e(u) ? u : f,
            y0: e(l) ? l : i,
          };
        return h()({}, p, t);
      }
      function g(t, e) {
        var n = t.scale,
          r = t.polar,
          o = t.horizontal,
          a = m(e),
          i = t.origin || { x: 0, y: 0 },
          c = o ? n.y(a.y) : n.x(a.x),
          l = o ? n.y(a.y0) : n.x(a.x0),
          u = o ? n.x(a.x) : n.y(a.y),
          s = o ? n.x(a.x0) : n.y(a.y0);
        return {
          x: r ? u * Math.cos(c) + i.x : c,
          x0: r ? s * Math.cos(l) + i.x : l,
          y: r ? -u * Math.sin(c) + i.y : u,
          y0: r ? -s * Math.sin(l) + i.x : s,
        };
      }
      function b(t) {
        var e =
            t[
              arguments.length > 1 && void 0 !== arguments[1]
                ? arguments[1]
                : "padding"
            ],
          n = "number" === typeof e ? e : 0,
          r = "object" === typeof e ? e : {};
        return {
          top: r.top || n,
          bottom: r.bottom || n,
          left: r.left || n,
          right: r.right || n,
        };
      }
      function x(t) {
        return "tooltip" === (t && t.type && t.type.role);
      }
      function O(t, e) {
        var n = t.theme,
          r = void 0 === n ? {} : n,
          o = t.labelComponent,
          a = (r[e] && r[e].style) || {};
        if (!x(o)) return a;
        var i = (r.tooltip && r.tooltip.style) || {},
          c = h()({}, i, a.labels);
        return h()({}, { labels: c }, a);
      }
      function w(t, e) {
        var n = "100%",
          r = "100%";
        if (!t) return h()({ parent: { height: r, width: n } }, e);
        var o = t.data,
          a = t.labels,
          i = t.parent,
          c = (e && e.parent) || {},
          l = (e && e.labels) || {},
          u = (e && e.data) || {};
        return {
          parent: h()({}, i, c, { width: n, height: r }),
          labels: h()({}, a, l),
          data: h()({}, o, u),
        };
      }
      function C(t, e) {
        return p()(t) ? t(e) : t;
      }
      function S(t, e) {
        return e.disableInlineStyles
          ? {}
          : t &&
              o()(t).some(function (e) {
                return p()(t[e]);
              })
            ? o()(t).reduce(function (n, r) {
                return (n[r] = C(t[r], e)), n;
              }, {})
            : t;
      }
      function A(t) {
        return "number" === typeof t ? t * (Math.PI / 180) : t;
      }
      function j(t) {
        return "number" === typeof t ? t / (Math.PI / 180) : t;
      }
      function k(t) {
        var e = b(t),
          n = e.left,
          r = e.right,
          o = e.top,
          a = e.bottom,
          i = t.width,
          c = t.height;
        return Math.min(i - n - r, c - o - a) / 2;
      }
      function P(t) {
        var e = t.width,
          n = t.height,
          r = b(t),
          o = r.top,
          a = r.bottom,
          i = r.left,
          c = r.right,
          l = Math.min(e - i - c, n - o - a) / 2,
          u = e / 2 + i - c,
          s = n / 2 + o - a;
        return { x: u + l > e ? l + i - c : u, y: s + l > n ? l + o - a : s };
      }
      function E(t, e) {
        return t.range && t.range[e]
          ? t.range[e]
          : t.range && Array.isArray(t.range)
            ? t.range
            : t.polar
              ? (function (t, e) {
                  return "x" === e
                    ? [A(t.startAngle || 0), A(t.endAngle || 360)]
                    : [t.innerRadius || 0, k(t)];
                })(t, e)
              : (function (t, e) {
                  var n = "x" !== e,
                    r = b(t);
                  return n
                    ? [t.height - r.bottom, r.top]
                    : [r.left, t.width - r.right];
                })(t, e);
      }
      function M(t) {
        return p()(t)
          ? t
          : null === t || void 0 === t
            ? function (t) {
                return t;
              }
            : s()(t);
      }
      function T(t, e, n) {
        var r = y(t.theme && t.theme[n] ? t.theme[n] : {}, ["style"]),
          o = (function (t) {
            if (void 0 !== t.horizontal || !t.children) return t.horizontal;
            var e = function (t) {
              return t.reduce(function (t, n) {
                var r = n.props || {};
                return t || r.horizontal || !r.children
                  ? (t = t || r.horizontal)
                  : e(v.Children.toArray(r.children));
              }, !1);
            };
            return e(v.Children.toArray(t.children));
          })(t),
          a = void 0 === o ? {} : { horizontal: o };
        return h()(a, t, r, e);
      }
      function _(t, e) {
        return e ? ("x" === t ? "y" : "x") : t;
      }
      function L(t, e) {
        var n =
            arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : {},
          r =
            arguments.length > 3 && void 0 !== arguments[3] ? arguments[3] : [],
          o =
            arguments.length > 4 && void 0 !== arguments[4]
              ? arguments[4]
              : function (t, e) {
                  return t.concat(e);
                },
          a = [
            "data",
            "domain",
            "categories",
            "polar",
            "startAngle",
            "endAngle",
            "minDomain",
            "maxDomain",
            "horizontal",
          ],
          c = function (t, u, s) {
            return t.reduce(function (t, r, f) {
              var d = r.type && r.type.role,
                h = r.props.name || "".concat(d, "-").concat(u[f]);
              if (r.props && r.props.children) {
                var y = i()({}, r.props, l()(n, a)),
                  m =
                    r.type && "stack" === r.type.role && p()(r.type.getChildren)
                      ? r.type.getChildren(y)
                      : v.Children.toArray(r.props.children).map(function (t) {
                          var e = i()({}, t.props, l()(y, a));
                          return v.cloneElement(t, e);
                        }),
                  g = m.map(function (t, e) {
                    return "".concat(h, "-").concat(e);
                  }),
                  b = c(m, g, r);
                t = o(t, b);
              } else {
                var x = e(r, h, s);
                x && (t = o(t, x));
              }
              return t;
            }, r);
          },
          u = t.map(function (t, e) {
            return e;
          });
        return c(t, u);
      }
    },
    78457: (t, e, n) => {
      "use strict";
      n.d(e, { h: () => y });
      var r = n(14064),
        o = n.n(r),
        a = n(66933),
        i = n.n(a),
        c = n(72791),
        l = n(15896),
        u = n(5129);
      function s(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function f(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? s(Object(n), !0).forEach(function (e) {
                p(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : s(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function p(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      function d(t, e) {
        return (
          (function (t) {
            if (Array.isArray(t)) return t;
          })(t) ||
          (function (t, e) {
            var n =
              null == t
                ? null
                : ("undefined" !== typeof Symbol && t[Symbol.iterator]) ||
                  t["@@iterator"];
            if (null == n) return;
            var r,
              o,
              a = [],
              i = !0,
              c = !1;
            try {
              for (
                n = n.call(t);
                !(i = (r = n.next()).done) &&
                (a.push(r.value), !e || a.length !== e);
                i = !0
              );
            } catch (l) {
              (c = !0), (o = l);
            } finally {
              try {
                i || null == n.return || n.return();
              } finally {
                if (c) throw o;
              }
            }
            return a;
          })(t, e) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return h(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return h(t, e);
          })(t, e) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function h(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      var v = { nodesShouldLoad: !1, nodesDoneLoad: !1, animating: !0 },
        y = function () {
          var t =
              arguments.length > 0 && void 0 !== arguments[0]
                ? arguments[0]
                : v,
            e = d(c.useState(t), 2),
            n = e[0],
            r = e[1],
            a = c.useCallback(
              function (t) {
                r(function (e) {
                  return f(f({}, e), t);
                });
              },
              [r],
            ),
            s = c.useCallback(
              function (t, e, r) {
                if (null === t || void 0 === t || !t.animate)
                  return e.props.animate;
                var o = t.animate && t.animate.getTransitions,
                  c = (function () {
                    var t = n && n.childrenTransitions;
                    return (
                      (t = l.Jr(t) ? t[r] : t),
                      i()({ childrenTransitions: t }, n)
                    );
                  })(),
                  s = (t.animate && t.animate.parentState) || c;
                if (!o) {
                  var f = u.C(t, c, function (t) {
                    return a(t);
                  });
                  o = function (t) {
                    return f(t, r);
                  };
                }
                return i()(
                  { getTransitions: o, parentState: s },
                  t.animate,
                  e.props.animate,
                );
              },
              [n, a],
            ),
            p = c.useCallback(
              function (t, e) {
                if (null !== t && void 0 !== t && t.animate)
                  if (t.animate.parentState) {
                    var n = t.animate.parentState.nodesWillExit ? t : null,
                      r = i()(
                        { oldProps: n, nextProps: e },
                        t.animate.parentState,
                      );
                    a(r);
                  } else {
                    var s = c.Children.toArray(t.children),
                      f = c.Children.toArray(e.children),
                      p = function (t) {
                        var e = function (t) {
                          return t.type && t.type.continuous;
                        };
                        return Array.isArray(t) ? o()(t, e) : e(t);
                      },
                      d =
                        !t.polar &&
                        o()(s, function (t) {
                          return (
                            p(t) || (t.props.children && p(t.props.children))
                          );
                        }),
                      h = u.A(s, f),
                      v = h.nodesWillExit,
                      y = h.nodesWillEnter,
                      m = h.childrenTransitions,
                      g = h.nodesShouldEnter;
                    a({
                      nodesWillExit: v,
                      nodesWillEnter: y,
                      nodesShouldEnter: g,
                      childrenTransitions: l.Jr(m) ? m[0] : m,
                      oldProps: v ? t : void 0,
                      nextProps: e,
                      continuous: d,
                    });
                  }
              },
              [a],
            ),
            h = c.useCallback(
              function (t) {
                return (n && n.nodesWillExit && n.oldProps) || t;
              },
              [n],
            );
          return {
            state: n,
            setState: a,
            getAnimationProps: s,
            setAnimationState: p,
            getProps: h,
          };
        };
    },
    70295: (t, e, n) => {
      "use strict";
      n.d(e, { Y: () => o });
      var r = n(72791);
      function o(t) {
        var e = r.useRef();
        return (
          r.useEffect(function () {
            e.current = t;
          }),
          e.current
        );
      }
    },
    21222: (t, e, n) => {
      "use strict";
      n.d(e, {
        AM: () => h,
        Nf: () => s,
        Q: () => u,
        Sw: () => p,
        nV: () => f,
        ow: () => d,
      });
      var r = n(66933),
        o = n.n(r),
        a = n(8091);
      function i(t, e) {
        if (t.polar) return {};
        var n = (function (t, e) {
          e = e || {};
          var n = t.horizontal,
            r = t.style.labels || {},
            o = a.xs(r.padding, t) || 0,
            i = e._y < 0 ? -1 : 1;
          return { x: n ? i * o : 0, y: n ? 0 : -1 * i * o };
        })(t, e);
        return { dx: n.x, dy: n.y };
      }
      function c(t, e) {
        var n = t.polar,
          r = a.q2(t, e),
          o = r.x,
          i = r.y;
        if (!n) return { x: o, y: i };
        var c = (function (t, e) {
          var n = t.style,
            r = d(t, e),
            o = n.labels || {},
            i = a.xs(o.padding, t) || 0,
            c = a.Ht(r);
          return { x: i * Math.cos(c), y: -i * Math.sin(c) };
        })(t, e);
        return { x: o + c.x, y: i + c.y };
      }
      function l(t) {
        var e = t.labelComponent,
          n = t.labelPlacement,
          r = t.polar ? "perpendicular" : "vertical";
        return n || (e.props && e.props.labelPlacement) || r;
      }
      function u(t, e, n) {
        return void 0 !== (e = e || {}).label
          ? e.label
          : Array.isArray(t.labels)
            ? t.labels[n]
            : t.labels;
      }
      function s(t, e) {
        var n = l(t);
        return "perpendicular" === n ||
          ("vertical" === n && (90 === e || 270 === e))
          ? "middle"
          : e <= 90 || e > 270
            ? "start"
            : "end";
      }
      function f(t, e) {
        var n = l(t),
          r = (function (t) {
            return t < 45 || t > 315
              ? "right"
              : t >= 45 && t <= 135
                ? "top"
                : t > 135 && t < 225
                  ? "left"
                  : "bottom";
          })(e);
        return "parallel" === n || "left" === r || "right" === r
          ? "middle"
          : "top" === r
            ? "end"
            : "start";
      }
      function p(t, e) {
        var n = t.labelPlacement,
          r = t.datum;
        if (!n || "vertical" === n) return 0;
        var o = void 0 !== e ? e % 360 : d(t, r),
          a = 0;
        return (
          0 === o || 180 === o
            ? (a = 90)
            : o > 0 && o < 180
              ? (a = 90 - o)
              : o > 180 && o < 360 && (a = 270 - o),
          a +
            ((o > 90 && o < 180) || o > 270 ? 1 : -1) *
              ("perpendicular" === n ? 0 : 90)
        );
      }
      function d(t, e) {
        var n = a.F8(e).x;
        return a.vi(t.scale.x(n)) % 360;
      }
      function h(t, e) {
        var n = t.scale,
          r = t.data,
          p = t.style,
          h = t.horizontal,
          v = t.polar,
          y = t.width,
          m = t.height,
          g = t.theme,
          b = t.labelComponent,
          x = t.disableInlineStyles,
          O = r[e],
          w = d(t, O),
          C = v
            ? s(t, w)
            : (function (t, e) {
                e = e || {};
                var n = t.style,
                  r = t.horizontal,
                  o = e._y >= 0 ? 1 : -1,
                  a = (n && n.labels) || {};
                return e.verticalAnchor || a.verticalAnchor
                  ? e.verticalAnchor || a.verticalAnchor
                  : r
                    ? o >= 0
                      ? "start"
                      : "end"
                    : "middle";
              })(t, O),
          S = v
            ? f(t, w)
            : (function (t, e) {
                var n = (e = e || {})._y >= 0 ? 1 : -1,
                  r = (t.style && t.style.labels) || {};
                return e.verticalAnchor || r.verticalAnchor
                  ? e.verticalAnchor || r.verticalAnchor
                  : t.horizontal
                    ? "middle"
                    : n >= 0
                      ? "end"
                      : "start";
              })(t, O),
          A = (function (t, e) {
            e = e || {};
            var n = (t.style && t.style.labels) || {};
            return void 0 === e.angle ? n.angle : e.angle;
          })(t, O),
          j = u(t, O, e),
          k = l(t),
          P = c(t, O),
          E = P.x,
          M = P.y,
          T = i(t, O),
          _ = {
            angle: A,
            data: r,
            datum: O,
            disableInlineStyles: x,
            horizontal: h,
            index: e,
            polar: v,
            scale: n,
            labelPlacement: k,
            text: j,
            textAnchor: C,
            verticalAnchor: S,
            x: E,
            y: M,
            dx: T.dx,
            dy: T.dy,
            width: y,
            height: m,
            style: p.labels,
          };
        if (!a.ij(b)) return _;
        var L = (g && g.tooltip) || {};
        return o()({}, _, a.CE(L, ["style"]));
      }
    },
    40143: (t, e, n) => {
      "use strict";
      function r(t) {
        0;
      }
      n.d(e, { Z: () => r });
    },
    42745: (t, e, n) => {
      "use strict";
      n.d(e, {
        A7: () => h,
        BO: () => d,
        KO: () => y,
        _L: () => v,
        bA: () => g,
        nw: () => m,
        xx: () => b,
      });
      var r = n(65625),
        o = n.n(r),
        a = n(61211),
        i = n.n(a),
        c = n(20933);
      var l = function (t) {
          var e = function (e) {
            return function (n, r, o) {
              var a = n[r];
              if (void 0 === a || null === a)
                return e
                  ? new Error(
                      "Required `"
                        .concat(r, "` was not specified in `")
                        .concat(o, "`."),
                    )
                  : null;
              for (
                var i = arguments.length,
                  c = new Array(i > 3 ? i - 3 : 0),
                  l = 3;
                l < i;
                l++
              )
                c[l - 3] = arguments[l];
              return t.apply(void 0, [n, r, o].concat(c));
            };
          };
          return Object.assign(e(!1), { isRequired: e(!0) });
        },
        u = function () {
          return null;
        },
        s = function () {},
        f = function (t) {
          return void 0 === t ? s : null === t ? u : t.constructor;
        },
        p = function (t) {
          return void 0 === t
            ? "undefined"
            : null === t
              ? "null"
              : Object.prototype.toString.call(t).slice(8, -1);
        };
      function d(t) {
        return l(function (e, n, r) {
          for (
            var o = arguments.length, a = new Array(o > 3 ? o - 3 : 0), i = 3;
            i < o;
            i++
          )
            a[i - 3] = arguments[i];
          return t.reduce(function (t, o) {
            return t || o.apply(void 0, [e, n, r].concat(a));
          }, null);
        });
      }
      var h = l(function (t, e, n) {
          var r = t[e];
          return "number" !== typeof r || r < 0
            ? new Error(
                "`"
                  .concat(e, "` in `")
                  .concat(n, "` must be a non-negative number."),
              )
            : null;
        }),
        v = l(function (t, e, n) {
          var r = t[e];
          return "number" !== typeof r || r % 1 !== 0
            ? new Error(
                "`".concat(e, "` in `").concat(n, "` must be an integer."),
              )
            : null;
        }),
        y = l(function (t, e, n) {
          var r = t[e];
          return "number" !== typeof r || r <= 0
            ? new Error(
                "`"
                  .concat(e, "` in `")
                  .concat(n, "` must be a number greater than zero."),
              )
            : null;
        }),
        m = l(function (t, e, n) {
          var r = t[e];
          return Array.isArray(r) && 2 === r.length && r[1] !== r[0]
            ? null
            : new Error(
                "`"
                  .concat(e, "` in `")
                  .concat(
                    n,
                    "` must be an array of two unique numeric values.",
                  ),
              );
        }),
        g = l(function (t, e, n) {
          var r = t[e];
          return c.sB(r)
            ? null
            : new Error(
                "`".concat(e, "` in `").concat(n, "` must be a d3 scale."),
              );
        }),
        b = l(function (t, e, n) {
          var r = t[e];
          if (!Array.isArray(r))
            return new Error(
              "`".concat(e, "` in `").concat(n, "` must be an array."),
            );
          if (r.length < 2) return null;
          var o = f(r[0]),
            a = i()(r, function (t) {
              return o !== f(t);
            });
          if (a) {
            var c = p(r[0]),
              l = p(a);
            return new Error(
              "Expected `".concat(e, "` in `").concat(n, "` to be a ") +
                "homogeneous array, but found types `".concat(c, "` and ") +
                "`".concat(l, "`."),
            );
          }
          return null;
        });
      l(function (t, e) {
        return t[e] && Array.isArray(t[e]) && t[e].length !== t.data.length
          ? new Error("Length of data and ".concat(e, " arrays must match."))
          : null;
      }),
        l(function (t, e, n) {
          return t[e] && !o()(t[e])
            ? new Error(
                "`"
                  .concat(e, "` in `")
                  .concat(n, "` must be a regular expression."),
              )
            : null;
        });
    },
    20933: (t, e, n) => {
      "use strict";
      n.d(e, {
        q8: () => _r,
        w8: () => Tr,
        j$: () => Lr,
        md: () => Dr,
        oL: () => Rr,
        sB: () => Pr,
      });
      var r = {};
      n.r(r),
        n.d(r, {
          scaleBand: () => O,
          scaleDiverging: () => wr,
          scaleDivergingLog: () => Cr,
          scaleDivergingPow: () => Ar,
          scaleDivergingSqrt: () => jr,
          scaleDivergingSymlog: () => Sr,
          scaleIdentity: () => vt,
          scaleImplicit: () => b,
          scaleLinear: () => ht,
          scaleLog: () => St,
          scaleOrdinal: () => x,
          scalePoint: () => C,
          scalePow: () => Lt,
          scaleQuantile: () => Vt,
          scaleQuantize: () => $t,
          scaleRadial: () => Rt,
          scaleSequential: () => vr,
          scaleSequentialLog: () => yr,
          scaleSequentialPow: () => gr,
          scaleSequentialQuantile: () => xr,
          scaleSequentialSqrt: () => br,
          scaleSequentialSymlog: () => mr,
          scaleSqrt: () => Dt,
          scaleSymlog: () => Pt,
          scaleThreshold: () => Yt,
          scaleTime: () => fr,
          scaleUtc: () => pr,
          tickFormat: () => pt,
        });
      var o = n(93977),
        a = n.n(o),
        i = n(74786),
        c = n.n(i),
        l = n(40806),
        u = n.n(l),
        s = n(8091),
        f = n(15896);
      function p(t, e) {
        switch (arguments.length) {
          case 0:
            break;
          case 1:
            this.range(t);
            break;
          default:
            this.range(e).domain(t);
        }
        return this;
      }
      function d(t, e) {
        switch (arguments.length) {
          case 0:
            break;
          case 1:
            "function" === typeof t ? this.interpolator(t) : this.range(t);
            break;
          default:
            this.domain(t),
              "function" === typeof e ? this.interpolator(e) : this.range(e);
        }
        return this;
      }
      class h extends Map {
        constructor(t) {
          let e =
            arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : g;
          if (
            (super(),
            Object.defineProperties(this, {
              _intern: { value: new Map() },
              _key: { value: e },
            }),
            null != t)
          )
            for (const [n, r] of t) this.set(n, r);
        }
        get(t) {
          return super.get(v(this, t));
        }
        has(t) {
          return super.has(v(this, t));
        }
        set(t, e) {
          return super.set(y(this, t), e);
        }
        delete(t) {
          return super.delete(m(this, t));
        }
      }
      function v(t, e) {
        let { _intern: n, _key: r } = t;
        const o = r(e);
        return n.has(o) ? n.get(o) : e;
      }
      function y(t, e) {
        let { _intern: n, _key: r } = t;
        const o = r(e);
        return n.has(o) ? n.get(o) : (n.set(o, e), e);
      }
      function m(t, e) {
        let { _intern: n, _key: r } = t;
        const o = r(e);
        return n.has(o) && ((e = n.get(o)), n.delete(o)), e;
      }
      function g(t) {
        return null !== t && "object" === typeof t ? t.valueOf() : t;
      }
      const b = Symbol("implicit");
      function x() {
        var t = new h(),
          e = [],
          n = [],
          r = b;
        function o(o) {
          let a = t.get(o);
          if (void 0 === a) {
            if (r !== b) return r;
            t.set(o, (a = e.push(o) - 1));
          }
          return n[a % n.length];
        }
        return (
          (o.domain = function (n) {
            if (!arguments.length) return e.slice();
            (e = []), (t = new h());
            for (const r of n) t.has(r) || t.set(r, e.push(r) - 1);
            return o;
          }),
          (o.range = function (t) {
            return arguments.length ? ((n = Array.from(t)), o) : n.slice();
          }),
          (o.unknown = function (t) {
            return arguments.length ? ((r = t), o) : r;
          }),
          (o.copy = function () {
            return x(e, n).unknown(r);
          }),
          p.apply(o, arguments),
          o
        );
      }
      function O() {
        var t,
          e,
          n = x().unknown(void 0),
          r = n.domain,
          o = n.range,
          a = 0,
          i = 1,
          c = !1,
          l = 0,
          u = 0,
          s = 0.5;
        function f() {
          var n = r().length,
            f = i < a,
            p = f ? i : a,
            d = f ? a : i;
          (t = (d - p) / Math.max(1, n - l + 2 * u)),
            c && (t = Math.floor(t)),
            (p += (d - p - t * (n - l)) * s),
            (e = t * (1 - l)),
            c && ((p = Math.round(p)), (e = Math.round(e)));
          var h = (function (t, e, n) {
            (t = +t),
              (e = +e),
              (n =
                (o = arguments.length) < 2
                  ? ((e = t), (t = 0), 1)
                  : o < 3
                    ? 1
                    : +n);
            for (
              var r = -1,
                o = 0 | Math.max(0, Math.ceil((e - t) / n)),
                a = new Array(o);
              ++r < o;

            )
              a[r] = t + r * n;
            return a;
          })(n).map(function (e) {
            return p + t * e;
          });
          return o(f ? h.reverse() : h);
        }
        return (
          delete n.unknown,
          (n.domain = function (t) {
            return arguments.length ? (r(t), f()) : r();
          }),
          (n.range = function (t) {
            return arguments.length
              ? (([a, i] = t), (a = +a), (i = +i), f())
              : [a, i];
          }),
          (n.rangeRound = function (t) {
            return ([a, i] = t), (a = +a), (i = +i), (c = !0), f();
          }),
          (n.bandwidth = function () {
            return e;
          }),
          (n.step = function () {
            return t;
          }),
          (n.round = function (t) {
            return arguments.length ? ((c = !!t), f()) : c;
          }),
          (n.padding = function (t) {
            return arguments.length ? ((l = Math.min(1, (u = +t))), f()) : l;
          }),
          (n.paddingInner = function (t) {
            return arguments.length ? ((l = Math.min(1, t)), f()) : l;
          }),
          (n.paddingOuter = function (t) {
            return arguments.length ? ((u = +t), f()) : u;
          }),
          (n.align = function (t) {
            return arguments.length
              ? ((s = Math.max(0, Math.min(1, t))), f())
              : s;
          }),
          (n.copy = function () {
            return O(r(), [a, i])
              .round(c)
              .paddingInner(l)
              .paddingOuter(u)
              .align(s);
          }),
          p.apply(f(), arguments)
        );
      }
      function w(t) {
        var e = t.copy;
        return (
          (t.padding = t.paddingOuter),
          delete t.paddingInner,
          delete t.paddingOuter,
          (t.copy = function () {
            return w(e());
          }),
          t
        );
      }
      function C() {
        return w(O.apply(null, arguments).paddingInner(1));
      }
      const S = Math.sqrt(50),
        A = Math.sqrt(10),
        j = Math.sqrt(2);
      function k(t, e, n) {
        const r = (e - t) / Math.max(0, n),
          o = Math.floor(Math.log10(r)),
          a = r / Math.pow(10, o),
          i = a >= S ? 10 : a >= A ? 5 : a >= j ? 2 : 1;
        let c, l, u;
        return (
          o < 0
            ? ((u = Math.pow(10, -o) / i),
              (c = Math.round(t * u)),
              (l = Math.round(e * u)),
              c / u < t && ++c,
              l / u > e && --l,
              (u = -u))
            : ((u = Math.pow(10, o) * i),
              (c = Math.round(t / u)),
              (l = Math.round(e / u)),
              c * u < t && ++c,
              l * u > e && --l),
          l < c && 0.5 <= n && n < 2 ? k(t, e, 2 * n) : [c, l, u]
        );
      }
      function P(t, e, n) {
        if (!((n = +n) > 0)) return [];
        if ((t = +t) === (e = +e)) return [t];
        const r = e < t,
          [o, a, i] = r ? k(e, t, n) : k(t, e, n);
        if (!(a >= o)) return [];
        const c = a - o + 1,
          l = new Array(c);
        if (r)
          if (i < 0) for (let u = 0; u < c; ++u) l[u] = (a - u) / -i;
          else for (let u = 0; u < c; ++u) l[u] = (a - u) * i;
        else if (i < 0) for (let u = 0; u < c; ++u) l[u] = (o + u) / -i;
        else for (let u = 0; u < c; ++u) l[u] = (o + u) * i;
        return l;
      }
      function E(t, e, n) {
        return k((t = +t), (e = +e), (n = +n))[2];
      }
      function M(t, e, n) {
        n = +n;
        const r = (e = +e) < (t = +t),
          o = r ? E(e, t, n) : E(t, e, n);
        return (r ? -1 : 1) * (o < 0 ? 1 / -o : o);
      }
      function T(t, e) {
        return null == t || null == e
          ? NaN
          : t < e
            ? -1
            : t > e
              ? 1
              : t >= e
                ? 0
                : NaN;
      }
      function _(t, e) {
        return null == t || null == e
          ? NaN
          : e < t
            ? -1
            : e > t
              ? 1
              : e >= t
                ? 0
                : NaN;
      }
      function L(t) {
        let e, n, r;
        function o(t, r) {
          let o =
              arguments.length > 2 && void 0 !== arguments[2]
                ? arguments[2]
                : 0,
            a =
              arguments.length > 3 && void 0 !== arguments[3]
                ? arguments[3]
                : t.length;
          if (o < a) {
            if (0 !== e(r, r)) return a;
            do {
              const e = (o + a) >>> 1;
              n(t[e], r) < 0 ? (o = e + 1) : (a = e);
            } while (o < a);
          }
          return o;
        }
        return (
          2 !== t.length
            ? ((e = T), (n = (e, n) => T(t(e), n)), (r = (e, n) => t(e) - n))
            : ((e = t === T || t === _ ? t : D), (n = t), (r = t)),
          {
            left: o,
            center: function (t, e) {
              let n =
                arguments.length > 2 && void 0 !== arguments[2]
                  ? arguments[2]
                  : 0;
              const a = o(
                t,
                e,
                n,
                (arguments.length > 3 && void 0 !== arguments[3]
                  ? arguments[3]
                  : t.length) - 1,
              );
              return a > n && r(t[a - 1], e) > -r(t[a], e) ? a - 1 : a;
            },
            right: function (t, r) {
              let o =
                  arguments.length > 2 && void 0 !== arguments[2]
                    ? arguments[2]
                    : 0,
                a =
                  arguments.length > 3 && void 0 !== arguments[3]
                    ? arguments[3]
                    : t.length;
              if (o < a) {
                if (0 !== e(r, r)) return a;
                do {
                  const e = (o + a) >>> 1;
                  n(t[e], r) <= 0 ? (o = e + 1) : (a = e);
                } while (o < a);
              }
              return o;
            },
          }
        );
      }
      function D() {
        return 0;
      }
      function I(t) {
        return null === t ? NaN : +t;
      }
      const R = L(T),
        N = R.right,
        W = (R.left, L(I).center, N);
      var F = n(67536),
        z = n(14837);
      function U(t, e) {
        return (
          (t = +t),
          (e = +e),
          function (n) {
            return Math.round(t * (1 - n) + e * n);
          }
        );
      }
      function B(t) {
        return +t;
      }
      var q = [0, 1];
      function H(t) {
        return t;
      }
      function V(t, e) {
        return (e -= t = +t)
          ? function (n) {
              return (n - t) / e;
            }
          : ((n = isNaN(e) ? NaN : 0.5),
            function () {
              return n;
            });
        var n;
      }
      function $(t, e, n) {
        var r = t[0],
          o = t[1],
          a = e[0],
          i = e[1];
        return (
          o < r
            ? ((r = V(o, r)), (a = n(i, a)))
            : ((r = V(r, o)), (a = n(a, i))),
          function (t) {
            return a(r(t));
          }
        );
      }
      function Y(t, e, n) {
        var r = Math.min(t.length, e.length) - 1,
          o = new Array(r),
          a = new Array(r),
          i = -1;
        for (
          t[r] < t[0] && ((t = t.slice().reverse()), (e = e.slice().reverse()));
          ++i < r;

        )
          (o[i] = V(t[i], t[i + 1])), (a[i] = n(e[i], e[i + 1]));
        return function (e) {
          var n = W(t, e, 1, r) - 1;
          return a[n](o[n](e));
        };
      }
      function Z(t, e) {
        return e
          .domain(t.domain())
          .range(t.range())
          .interpolate(t.interpolate())
          .clamp(t.clamp())
          .unknown(t.unknown());
      }
      function K() {
        var t,
          e,
          n,
          r,
          o,
          a,
          i = q,
          c = q,
          l = F.Z,
          u = H;
        function s() {
          var t = Math.min(i.length, c.length);
          return (
            u !== H &&
              (u = (function (t, e) {
                var n;
                return (
                  t > e && ((n = t), (t = e), (e = n)),
                  function (n) {
                    return Math.max(t, Math.min(e, n));
                  }
                );
              })(i[0], i[t - 1])),
            (r = t > 2 ? Y : $),
            (o = a = null),
            f
          );
        }
        function f(e) {
          return null == e || isNaN((e = +e))
            ? n
            : (o || (o = r(i.map(t), c, l)))(t(u(e)));
        }
        return (
          (f.invert = function (n) {
            return u(e((a || (a = r(c, i.map(t), z.Z)))(n)));
          }),
          (f.domain = function (t) {
            return arguments.length ? ((i = Array.from(t, B)), s()) : i.slice();
          }),
          (f.range = function (t) {
            return arguments.length ? ((c = Array.from(t)), s()) : c.slice();
          }),
          (f.rangeRound = function (t) {
            return (c = Array.from(t)), (l = U), s();
          }),
          (f.clamp = function (t) {
            return arguments.length ? ((u = !!t || H), s()) : u !== H;
          }),
          (f.interpolate = function (t) {
            return arguments.length ? ((l = t), s()) : l;
          }),
          (f.unknown = function (t) {
            return arguments.length ? ((n = t), f) : n;
          }),
          function (n, r) {
            return (t = n), (e = r), s();
          }
        );
      }
      function G() {
        return K()(H, H);
      }
      var X,
        Q =
          /^(?:(.)?([<>=^]))?([+\-( ])?([$#])?(0)?(\d+)?(,)?(\.\d+)?(~)?([a-z%])?$/i;
      function J(t) {
        if (!(e = Q.exec(t))) throw new Error("invalid format: " + t);
        var e;
        return new tt({
          fill: e[1],
          align: e[2],
          sign: e[3],
          symbol: e[4],
          zero: e[5],
          width: e[6],
          comma: e[7],
          precision: e[8] && e[8].slice(1),
          trim: e[9],
          type: e[10],
        });
      }
      function tt(t) {
        (this.fill = void 0 === t.fill ? " " : t.fill + ""),
          (this.align = void 0 === t.align ? ">" : t.align + ""),
          (this.sign = void 0 === t.sign ? "-" : t.sign + ""),
          (this.symbol = void 0 === t.symbol ? "" : t.symbol + ""),
          (this.zero = !!t.zero),
          (this.width = void 0 === t.width ? void 0 : +t.width),
          (this.comma = !!t.comma),
          (this.precision = void 0 === t.precision ? void 0 : +t.precision),
          (this.trim = !!t.trim),
          (this.type = void 0 === t.type ? "" : t.type + "");
      }
      function et(t, e) {
        if (
          (n = (t = e ? t.toExponential(e - 1) : t.toExponential()).indexOf(
            "e",
          )) < 0
        )
          return null;
        var n,
          r = t.slice(0, n);
        return [r.length > 1 ? r[0] + r.slice(2) : r, +t.slice(n + 1)];
      }
      function nt(t) {
        return (t = et(Math.abs(t))) ? t[1] : NaN;
      }
      function rt(t, e) {
        var n = et(t, e);
        if (!n) return t + "";
        var r = n[0],
          o = n[1];
        return o < 0
          ? "0." + new Array(-o).join("0") + r
          : r.length > o + 1
            ? r.slice(0, o + 1) + "." + r.slice(o + 1)
            : r + new Array(o - r.length + 2).join("0");
      }
      (J.prototype = tt.prototype),
        (tt.prototype.toString = function () {
          return (
            this.fill +
            this.align +
            this.sign +
            this.symbol +
            (this.zero ? "0" : "") +
            (void 0 === this.width ? "" : Math.max(1, 0 | this.width)) +
            (this.comma ? "," : "") +
            (void 0 === this.precision
              ? ""
              : "." + Math.max(0, 0 | this.precision)) +
            (this.trim ? "~" : "") +
            this.type
          );
        });
      const ot = {
        "%": (t, e) => (100 * t).toFixed(e),
        b: (t) => Math.round(t).toString(2),
        c: (t) => t + "",
        d: function (t) {
          return Math.abs((t = Math.round(t))) >= 1e21
            ? t.toLocaleString("en").replace(/,/g, "")
            : t.toString(10);
        },
        e: (t, e) => t.toExponential(e),
        f: (t, e) => t.toFixed(e),
        g: (t, e) => t.toPrecision(e),
        o: (t) => Math.round(t).toString(8),
        p: (t, e) => rt(100 * t, e),
        r: rt,
        s: function (t, e) {
          var n = et(t, e);
          if (!n) return t + "";
          var r = n[0],
            o = n[1],
            a = o - (X = 3 * Math.max(-8, Math.min(8, Math.floor(o / 3)))) + 1,
            i = r.length;
          return a === i
            ? r
            : a > i
              ? r + new Array(a - i + 1).join("0")
              : a > 0
                ? r.slice(0, a) + "." + r.slice(a)
                : "0." +
                  new Array(1 - a).join("0") +
                  et(t, Math.max(0, e + a - 1))[0];
        },
        X: (t) => Math.round(t).toString(16).toUpperCase(),
        x: (t) => Math.round(t).toString(16),
      };
      function at(t) {
        return t;
      }
      var it,
        ct,
        lt,
        ut = Array.prototype.map,
        st = [
          "y",
          "z",
          "a",
          "f",
          "p",
          "n",
          "\xb5",
          "m",
          "",
          "k",
          "M",
          "G",
          "T",
          "P",
          "E",
          "Z",
          "Y",
        ];
      function ft(t) {
        var e,
          n,
          r =
            void 0 === t.grouping || void 0 === t.thousands
              ? at
              : ((e = ut.call(t.grouping, Number)),
                (n = t.thousands + ""),
                function (t, r) {
                  for (
                    var o = t.length, a = [], i = 0, c = e[0], l = 0;
                    o > 0 &&
                    c > 0 &&
                    (l + c + 1 > r && (c = Math.max(1, r - l)),
                    a.push(t.substring((o -= c), o + c)),
                    !((l += c + 1) > r));

                  )
                    c = e[(i = (i + 1) % e.length)];
                  return a.reverse().join(n);
                }),
          o = void 0 === t.currency ? "" : t.currency[0] + "",
          a = void 0 === t.currency ? "" : t.currency[1] + "",
          i = void 0 === t.decimal ? "." : t.decimal + "",
          c =
            void 0 === t.numerals
              ? at
              : (function (t) {
                  return function (e) {
                    return e.replace(/[0-9]/g, function (e) {
                      return t[+e];
                    });
                  };
                })(ut.call(t.numerals, String)),
          l = void 0 === t.percent ? "%" : t.percent + "",
          u = void 0 === t.minus ? "\u2212" : t.minus + "",
          s = void 0 === t.nan ? "NaN" : t.nan + "";
        function f(t) {
          var e = (t = J(t)).fill,
            n = t.align,
            f = t.sign,
            p = t.symbol,
            d = t.zero,
            h = t.width,
            v = t.comma,
            y = t.precision,
            m = t.trim,
            g = t.type;
          "n" === g
            ? ((v = !0), (g = "g"))
            : ot[g] || (void 0 === y && (y = 12), (m = !0), (g = "g")),
            (d || ("0" === e && "=" === n)) && ((d = !0), (e = "0"), (n = "="));
          var b =
              "$" === p
                ? o
                : "#" === p && /[boxX]/.test(g)
                  ? "0" + g.toLowerCase()
                  : "",
            x = "$" === p ? a : /[%p]/.test(g) ? l : "",
            O = ot[g],
            w = /[defgprs%]/.test(g);
          function C(t) {
            var o,
              a,
              l,
              p = b,
              C = x;
            if ("c" === g) (C = O(t) + C), (t = "");
            else {
              var S = (t = +t) < 0 || 1 / t < 0;
              if (
                ((t = isNaN(t) ? s : O(Math.abs(t), y)),
                m &&
                  (t = (function (t) {
                    t: for (var e, n = t.length, r = 1, o = -1; r < n; ++r)
                      switch (t[r]) {
                        case ".":
                          o = e = r;
                          break;
                        case "0":
                          0 === o && (o = r), (e = r);
                          break;
                        default:
                          if (!+t[r]) break t;
                          o > 0 && (o = 0);
                      }
                    return o > 0 ? t.slice(0, o) + t.slice(e + 1) : t;
                  })(t)),
                S && 0 === +t && "+" !== f && (S = !1),
                (p =
                  (S ? ("(" === f ? f : u) : "-" === f || "(" === f ? "" : f) +
                  p),
                (C =
                  ("s" === g ? st[8 + X / 3] : "") +
                  C +
                  (S && "(" === f ? ")" : "")),
                w)
              )
                for (o = -1, a = t.length; ++o < a; )
                  if (48 > (l = t.charCodeAt(o)) || l > 57) {
                    (C = (46 === l ? i + t.slice(o + 1) : t.slice(o)) + C),
                      (t = t.slice(0, o));
                    break;
                  }
            }
            v && !d && (t = r(t, 1 / 0));
            var A = p.length + t.length + C.length,
              j = A < h ? new Array(h - A + 1).join(e) : "";
            switch (
              (v &&
                d &&
                ((t = r(j + t, j.length ? h - C.length : 1 / 0)), (j = "")),
              n)
            ) {
              case "<":
                t = p + t + C + j;
                break;
              case "=":
                t = p + j + t + C;
                break;
              case "^":
                t = j.slice(0, (A = j.length >> 1)) + p + t + C + j.slice(A);
                break;
              default:
                t = j + p + t + C;
            }
            return c(t);
          }
          return (
            (y =
              void 0 === y
                ? 6
                : /[gprs]/.test(g)
                  ? Math.max(1, Math.min(21, y))
                  : Math.max(0, Math.min(20, y))),
            (C.toString = function () {
              return t + "";
            }),
            C
          );
        }
        return {
          format: f,
          formatPrefix: function (t, e) {
            var n = f((((t = J(t)).type = "f"), t)),
              r = 3 * Math.max(-8, Math.min(8, Math.floor(nt(e) / 3))),
              o = Math.pow(10, -r),
              a = st[8 + r / 3];
            return function (t) {
              return n(o * t) + a;
            };
          },
        };
      }
      function pt(t, e, n, r) {
        var o,
          a = M(t, e, n);
        switch ((r = J(null == r ? ",f" : r)).type) {
          case "s":
            var i = Math.max(Math.abs(t), Math.abs(e));
            return (
              null != r.precision ||
                isNaN(
                  (o = (function (t, e) {
                    return Math.max(
                      0,
                      3 * Math.max(-8, Math.min(8, Math.floor(nt(e) / 3))) -
                        nt(Math.abs(t)),
                    );
                  })(a, i)),
                ) ||
                (r.precision = o),
              lt(r, i)
            );
          case "":
          case "e":
          case "g":
          case "p":
          case "r":
            null != r.precision ||
              isNaN(
                (o = (function (t, e) {
                  return (
                    (t = Math.abs(t)),
                    (e = Math.abs(e) - t),
                    Math.max(0, nt(e) - nt(t)) + 1
                  );
                })(a, Math.max(Math.abs(t), Math.abs(e)))),
              ) ||
              (r.precision = o - ("e" === r.type));
            break;
          case "f":
          case "%":
            null != r.precision ||
              isNaN(
                (o = (function (t) {
                  return Math.max(0, -nt(Math.abs(t)));
                })(a)),
              ) ||
              (r.precision = o - 2 * ("%" === r.type));
        }
        return ct(r);
      }
      function dt(t) {
        var e = t.domain;
        return (
          (t.ticks = function (t) {
            var n = e();
            return P(n[0], n[n.length - 1], null == t ? 10 : t);
          }),
          (t.tickFormat = function (t, n) {
            var r = e();
            return pt(r[0], r[r.length - 1], null == t ? 10 : t, n);
          }),
          (t.nice = function (n) {
            null == n && (n = 10);
            var r,
              o,
              a = e(),
              i = 0,
              c = a.length - 1,
              l = a[i],
              u = a[c],
              s = 10;
            for (
              u < l && ((o = l), (l = u), (u = o), (o = i), (i = c), (c = o));
              s-- > 0;

            ) {
              if ((o = E(l, u, n)) === r) return (a[i] = l), (a[c] = u), e(a);
              if (o > 0)
                (l = Math.floor(l / o) * o), (u = Math.ceil(u / o) * o);
              else {
                if (!(o < 0)) break;
                (l = Math.ceil(l * o) / o), (u = Math.floor(u * o) / o);
              }
              r = o;
            }
            return t;
          }),
          t
        );
      }
      function ht() {
        var t = G();
        return (
          (t.copy = function () {
            return Z(t, ht());
          }),
          p.apply(t, arguments),
          dt(t)
        );
      }
      function vt(t) {
        var e;
        function n(t) {
          return null == t || isNaN((t = +t)) ? e : t;
        }
        return (
          (n.invert = n),
          (n.domain = n.range =
            function (e) {
              return arguments.length ? ((t = Array.from(e, B)), n) : t.slice();
            }),
          (n.unknown = function (t) {
            return arguments.length ? ((e = t), n) : e;
          }),
          (n.copy = function () {
            return vt(t).unknown(e);
          }),
          (t = arguments.length ? Array.from(t, B) : [0, 1]),
          dt(n)
        );
      }
      function yt(t, e) {
        var n,
          r = 0,
          o = (t = t.slice()).length - 1,
          a = t[r],
          i = t[o];
        return (
          i < a && ((n = r), (r = o), (o = n), (n = a), (a = i), (i = n)),
          (t[r] = e.floor(a)),
          (t[o] = e.ceil(i)),
          t
        );
      }
      function mt(t) {
        return Math.log(t);
      }
      function gt(t) {
        return Math.exp(t);
      }
      function bt(t) {
        return -Math.log(-t);
      }
      function xt(t) {
        return -Math.exp(-t);
      }
      function Ot(t) {
        return isFinite(t) ? +("1e" + t) : t < 0 ? 0 : t;
      }
      function wt(t) {
        return (e, n) => -t(-e, n);
      }
      function Ct(t) {
        const e = t(mt, gt),
          n = e.domain;
        let r,
          o,
          a = 10;
        function i() {
          return (
            (r = (function (t) {
              return t === Math.E
                ? Math.log
                : (10 === t && Math.log10) ||
                    (2 === t && Math.log2) ||
                    ((t = Math.log(t)), (e) => Math.log(e) / t);
            })(a)),
            (o = (function (t) {
              return 10 === t
                ? Ot
                : t === Math.E
                  ? Math.exp
                  : (e) => Math.pow(t, e);
            })(a)),
            n()[0] < 0 ? ((r = wt(r)), (o = wt(o)), t(bt, xt)) : t(mt, gt),
            e
          );
        }
        return (
          (e.base = function (t) {
            return arguments.length ? ((a = +t), i()) : a;
          }),
          (e.domain = function (t) {
            return arguments.length ? (n(t), i()) : n();
          }),
          (e.ticks = (t) => {
            const e = n();
            let i = e[0],
              c = e[e.length - 1];
            const l = c < i;
            l && ([i, c] = [c, i]);
            let u,
              s,
              f = r(i),
              p = r(c);
            const d = null == t ? 10 : +t;
            let h = [];
            if (!(a % 1) && p - f < d) {
              if (((f = Math.floor(f)), (p = Math.ceil(p)), i > 0)) {
                for (; f <= p; ++f)
                  for (u = 1; u < a; ++u)
                    if (((s = f < 0 ? u / o(-f) : u * o(f)), !(s < i))) {
                      if (s > c) break;
                      h.push(s);
                    }
              } else
                for (; f <= p; ++f)
                  for (u = a - 1; u >= 1; --u)
                    if (((s = f > 0 ? u / o(-f) : u * o(f)), !(s < i))) {
                      if (s > c) break;
                      h.push(s);
                    }
              2 * h.length < d && (h = P(i, c, d));
            } else h = P(f, p, Math.min(p - f, d)).map(o);
            return l ? h.reverse() : h;
          }),
          (e.tickFormat = (t, n) => {
            if (
              (null == t && (t = 10),
              null == n && (n = 10 === a ? "s" : ","),
              "function" !== typeof n &&
                (a % 1 || null != (n = J(n)).precision || (n.trim = !0),
                (n = ct(n))),
              t === 1 / 0)
            )
              return n;
            const i = Math.max(1, (a * t) / e.ticks().length);
            return (t) => {
              let e = t / o(Math.round(r(t)));
              return e * a < a - 0.5 && (e *= a), e <= i ? n(t) : "";
            };
          }),
          (e.nice = () =>
            n(
              yt(n(), {
                floor: (t) => o(Math.floor(r(t))),
                ceil: (t) => o(Math.ceil(r(t))),
              }),
            )),
          e
        );
      }
      function St() {
        const t = Ct(K()).domain([1, 10]);
        return (
          (t.copy = () => Z(t, St()).base(t.base())), p.apply(t, arguments), t
        );
      }
      function At(t) {
        return function (e) {
          return Math.sign(e) * Math.log1p(Math.abs(e / t));
        };
      }
      function jt(t) {
        return function (e) {
          return Math.sign(e) * Math.expm1(Math.abs(e)) * t;
        };
      }
      function kt(t) {
        var e = 1,
          n = t(At(e), jt(e));
        return (
          (n.constant = function (n) {
            return arguments.length ? t(At((e = +n)), jt(e)) : e;
          }),
          dt(n)
        );
      }
      function Pt() {
        var t = kt(K());
        return (
          (t.copy = function () {
            return Z(t, Pt()).constant(t.constant());
          }),
          p.apply(t, arguments)
        );
      }
      function Et(t) {
        return function (e) {
          return e < 0 ? -Math.pow(-e, t) : Math.pow(e, t);
        };
      }
      function Mt(t) {
        return t < 0 ? -Math.sqrt(-t) : Math.sqrt(t);
      }
      function Tt(t) {
        return t < 0 ? -t * t : t * t;
      }
      function _t(t) {
        var e = t(H, H),
          n = 1;
        return (
          (e.exponent = function (e) {
            return arguments.length
              ? 1 === (n = +e)
                ? t(H, H)
                : 0.5 === n
                  ? t(Mt, Tt)
                  : t(Et(n), Et(1 / n))
              : n;
          }),
          dt(e)
        );
      }
      function Lt() {
        var t = _t(K());
        return (
          (t.copy = function () {
            return Z(t, Lt()).exponent(t.exponent());
          }),
          p.apply(t, arguments),
          t
        );
      }
      function Dt() {
        return Lt.apply(null, arguments).exponent(0.5);
      }
      function It(t) {
        return Math.sign(t) * t * t;
      }
      function Rt() {
        var t,
          e = G(),
          n = [0, 1],
          r = !1;
        function o(n) {
          var o = (function (t) {
            return Math.sign(t) * Math.sqrt(Math.abs(t));
          })(e(n));
          return isNaN(o) ? t : r ? Math.round(o) : o;
        }
        return (
          (o.invert = function (t) {
            return e.invert(It(t));
          }),
          (o.domain = function (t) {
            return arguments.length ? (e.domain(t), o) : e.domain();
          }),
          (o.range = function (t) {
            return arguments.length
              ? (e.range((n = Array.from(t, B)).map(It)), o)
              : n.slice();
          }),
          (o.rangeRound = function (t) {
            return o.range(t).round(!0);
          }),
          (o.round = function (t) {
            return arguments.length ? ((r = !!t), o) : r;
          }),
          (o.clamp = function (t) {
            return arguments.length ? (e.clamp(t), o) : e.clamp();
          }),
          (o.unknown = function (e) {
            return arguments.length ? ((t = e), o) : t;
          }),
          (o.copy = function () {
            return Rt(e.domain(), n).round(r).clamp(e.clamp()).unknown(t);
          }),
          p.apply(o, arguments),
          dt(o)
        );
      }
      function Nt(t, e) {
        let n;
        if (void 0 === e)
          for (const r of t)
            null != r && (n < r || (void 0 === n && r >= r)) && (n = r);
        else {
          let r = -1;
          for (let o of t)
            null != (o = e(o, ++r, t)) &&
              (n < o || (void 0 === n && o >= o)) &&
              (n = o);
        }
        return n;
      }
      function Wt(t, e) {
        let n;
        if (void 0 === e)
          for (const r of t)
            null != r && (n > r || (void 0 === n && r >= r)) && (n = r);
        else {
          let r = -1;
          for (let o of t)
            null != (o = e(o, ++r, t)) &&
              (n > o || (void 0 === n && o >= o)) &&
              (n = o);
        }
        return n;
      }
      function Ft() {
        let t =
          arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : T;
        if (t === T) return zt;
        if ("function" !== typeof t)
          throw new TypeError("compare is not a function");
        return (e, n) => {
          const r = t(e, n);
          return r || 0 === r ? r : (0 === t(n, n)) - (0 === t(e, e));
        };
      }
      function zt(t, e) {
        return (
          (null == t || !(t >= t)) - (null == e || !(e >= e)) ||
          (t < e ? -1 : t > e ? 1 : 0)
        );
      }
      function Ut(t, e) {
        let n =
            arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : 0,
          r =
            arguments.length > 3 && void 0 !== arguments[3]
              ? arguments[3]
              : 1 / 0,
          o = arguments.length > 4 ? arguments[4] : void 0;
        if (
          ((e = Math.floor(e)),
          (n = Math.floor(Math.max(0, n))),
          (r = Math.floor(Math.min(t.length - 1, r))),
          !(n <= e && e <= r))
        )
          return t;
        for (o = void 0 === o ? zt : Ft(o); r > n; ) {
          if (r - n > 600) {
            const a = r - n + 1,
              i = e - n + 1,
              c = Math.log(a),
              l = 0.5 * Math.exp((2 * c) / 3),
              u =
                0.5 *
                Math.sqrt((c * l * (a - l)) / a) *
                (i - a / 2 < 0 ? -1 : 1);
            Ut(
              t,
              e,
              Math.max(n, Math.floor(e - (i * l) / a + u)),
              Math.min(r, Math.floor(e + ((a - i) * l) / a + u)),
              o,
            );
          }
          const a = t[e];
          let i = n,
            c = r;
          for (Bt(t, n, e), o(t[r], a) > 0 && Bt(t, n, r); i < c; ) {
            for (Bt(t, i, c), ++i, --c; o(t[i], a) < 0; ) ++i;
            for (; o(t[c], a) > 0; ) --c;
          }
          0 === o(t[n], a) ? Bt(t, n, c) : (++c, Bt(t, c, r)),
            c <= e && (n = c + 1),
            e <= c && (r = c - 1);
        }
        return t;
      }
      function Bt(t, e, n) {
        const r = t[e];
        (t[e] = t[n]), (t[n] = r);
      }
      function qt(t, e, n) {
        if (
          ((t = Float64Array.from(
            (function* (t, e) {
              if (void 0 === e)
                for (let n of t) null != n && (n = +n) >= n && (yield n);
              else {
                let n = -1;
                for (let r of t)
                  null != (r = e(r, ++n, t)) && (r = +r) >= r && (yield r);
              }
            })(t, n),
          )),
          (r = t.length) && !isNaN((e = +e)))
        ) {
          if (e <= 0 || r < 2) return Wt(t);
          if (e >= 1) return Nt(t);
          var r,
            o = (r - 1) * e,
            a = Math.floor(o),
            i = Nt(Ut(t, a).subarray(0, a + 1));
          return i + (Wt(t.subarray(a + 1)) - i) * (o - a);
        }
      }
      function Ht(t, e) {
        let n =
          arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : I;
        if ((r = t.length) && !isNaN((e = +e))) {
          if (e <= 0 || r < 2) return +n(t[0], 0, t);
          if (e >= 1) return +n(t[r - 1], r - 1, t);
          var r,
            o = (r - 1) * e,
            a = Math.floor(o),
            i = +n(t[a], a, t);
          return i + (+n(t[a + 1], a + 1, t) - i) * (o - a);
        }
      }
      function Vt() {
        var t,
          e = [],
          n = [],
          r = [];
        function o() {
          var t = 0,
            o = Math.max(1, n.length);
          for (r = new Array(o - 1); ++t < o; ) r[t - 1] = Ht(e, t / o);
          return a;
        }
        function a(e) {
          return null == e || isNaN((e = +e)) ? t : n[W(r, e)];
        }
        return (
          (a.invertExtent = function (t) {
            var o = n.indexOf(t);
            return o < 0
              ? [NaN, NaN]
              : [
                  o > 0 ? r[o - 1] : e[0],
                  o < r.length ? r[o] : e[e.length - 1],
                ];
          }),
          (a.domain = function (t) {
            if (!arguments.length) return e.slice();
            e = [];
            for (let n of t) null == n || isNaN((n = +n)) || e.push(n);
            return e.sort(T), o();
          }),
          (a.range = function (t) {
            return arguments.length ? ((n = Array.from(t)), o()) : n.slice();
          }),
          (a.unknown = function (e) {
            return arguments.length ? ((t = e), a) : t;
          }),
          (a.quantiles = function () {
            return r.slice();
          }),
          (a.copy = function () {
            return Vt().domain(e).range(n).unknown(t);
          }),
          p.apply(a, arguments)
        );
      }
      function $t() {
        var t,
          e = 0,
          n = 1,
          r = 1,
          o = [0.5],
          a = [0, 1];
        function i(e) {
          return null != e && e <= e ? a[W(o, e, 0, r)] : t;
        }
        function c() {
          var t = -1;
          for (o = new Array(r); ++t < r; )
            o[t] = ((t + 1) * n - (t - r) * e) / (r + 1);
          return i;
        }
        return (
          (i.domain = function (t) {
            return arguments.length
              ? (([e, n] = t), (e = +e), (n = +n), c())
              : [e, n];
          }),
          (i.range = function (t) {
            return arguments.length
              ? ((r = (a = Array.from(t)).length - 1), c())
              : a.slice();
          }),
          (i.invertExtent = function (t) {
            var i = a.indexOf(t);
            return i < 0
              ? [NaN, NaN]
              : i < 1
                ? [e, o[0]]
                : i >= r
                  ? [o[r - 1], n]
                  : [o[i - 1], o[i]];
          }),
          (i.unknown = function (e) {
            return arguments.length ? ((t = e), i) : i;
          }),
          (i.thresholds = function () {
            return o.slice();
          }),
          (i.copy = function () {
            return $t().domain([e, n]).range(a).unknown(t);
          }),
          p.apply(dt(i), arguments)
        );
      }
      function Yt() {
        var t,
          e = [0.5],
          n = [0, 1],
          r = 1;
        function o(o) {
          return null != o && o <= o ? n[W(e, o, 0, r)] : t;
        }
        return (
          (o.domain = function (t) {
            return arguments.length
              ? ((e = Array.from(t)), (r = Math.min(e.length, n.length - 1)), o)
              : e.slice();
          }),
          (o.range = function (t) {
            return arguments.length
              ? ((n = Array.from(t)), (r = Math.min(e.length, n.length - 1)), o)
              : n.slice();
          }),
          (o.invertExtent = function (t) {
            var r = n.indexOf(t);
            return [e[r - 1], e[r]];
          }),
          (o.unknown = function (e) {
            return arguments.length ? ((t = e), o) : t;
          }),
          (o.copy = function () {
            return Yt().domain(e).range(n).unknown(t);
          }),
          p.apply(o, arguments)
        );
      }
      (it = ft({ thousands: ",", grouping: [3], currency: ["$", ""] })),
        (ct = it.format),
        (lt = it.formatPrefix);
      const Zt = 1e3,
        Kt = 6e4,
        Gt = 36e5,
        Xt = 864e5,
        Qt = 6048e5,
        Jt = 2592e6,
        te = 31536e6,
        ee = new Date(),
        ne = new Date();
      function re(t, e, n, r) {
        function o(e) {
          return t((e = 0 === arguments.length ? new Date() : new Date(+e))), e;
        }
        return (
          (o.floor = (e) => (t((e = new Date(+e))), e)),
          (o.ceil = (n) => (t((n = new Date(n - 1))), e(n, 1), t(n), n)),
          (o.round = (t) => {
            const e = o(t),
              n = o.ceil(t);
            return t - e < n - t ? e : n;
          }),
          (o.offset = (t, n) => (
            e((t = new Date(+t)), null == n ? 1 : Math.floor(n)), t
          )),
          (o.range = (n, r, a) => {
            const i = [];
            if (
              ((n = o.ceil(n)),
              (a = null == a ? 1 : Math.floor(a)),
              !(n < r) || !(a > 0))
            )
              return i;
            let c;
            do {
              i.push((c = new Date(+n))), e(n, a), t(n);
            } while (c < n && n < r);
            return i;
          }),
          (o.filter = (n) =>
            re(
              (e) => {
                if (e >= e) for (; t(e), !n(e); ) e.setTime(e - 1);
              },
              (t, r) => {
                if (t >= t)
                  if (r < 0) for (; ++r <= 0; ) for (; e(t, -1), !n(t); );
                  else for (; --r >= 0; ) for (; e(t, 1), !n(t); );
              },
            )),
          n &&
            ((o.count = (e, r) => (
              ee.setTime(+e),
              ne.setTime(+r),
              t(ee),
              t(ne),
              Math.floor(n(ee, ne))
            )),
            (o.every = (t) => (
              (t = Math.floor(t)),
              isFinite(t) && t > 0
                ? t > 1
                  ? o.filter(
                      r
                        ? (e) => r(e) % t === 0
                        : (e) => o.count(0, e) % t === 0,
                    )
                  : o
                : null
            ))),
          o
        );
      }
      const oe = re(
        () => {},
        (t, e) => {
          t.setTime(+t + e);
        },
        (t, e) => e - t,
      );
      oe.every = (t) => (
        (t = Math.floor(t)),
        isFinite(t) && t > 0
          ? t > 1
            ? re(
                (e) => {
                  e.setTime(Math.floor(e / t) * t);
                },
                (e, n) => {
                  e.setTime(+e + n * t);
                },
                (e, n) => (n - e) / t,
              )
            : oe
          : null
      );
      oe.range;
      const ae = re(
          (t) => {
            t.setTime(t - t.getMilliseconds());
          },
          (t, e) => {
            t.setTime(+t + e * Zt);
          },
          (t, e) => (e - t) / Zt,
          (t) => t.getUTCSeconds(),
        ),
        ie =
          (ae.range,
          re(
            (t) => {
              t.setTime(t - t.getMilliseconds() - t.getSeconds() * Zt);
            },
            (t, e) => {
              t.setTime(+t + e * Kt);
            },
            (t, e) => (e - t) / Kt,
            (t) => t.getMinutes(),
          )),
        ce =
          (ie.range,
          re(
            (t) => {
              t.setUTCSeconds(0, 0);
            },
            (t, e) => {
              t.setTime(+t + e * Kt);
            },
            (t, e) => (e - t) / Kt,
            (t) => t.getUTCMinutes(),
          )),
        le =
          (ce.range,
          re(
            (t) => {
              t.setTime(
                t -
                  t.getMilliseconds() -
                  t.getSeconds() * Zt -
                  t.getMinutes() * Kt,
              );
            },
            (t, e) => {
              t.setTime(+t + e * Gt);
            },
            (t, e) => (e - t) / Gt,
            (t) => t.getHours(),
          )),
        ue =
          (le.range,
          re(
            (t) => {
              t.setUTCMinutes(0, 0, 0);
            },
            (t, e) => {
              t.setTime(+t + e * Gt);
            },
            (t, e) => (e - t) / Gt,
            (t) => t.getUTCHours(),
          )),
        se =
          (ue.range,
          re(
            (t) => t.setHours(0, 0, 0, 0),
            (t, e) => t.setDate(t.getDate() + e),
            (t, e) =>
              (e - t - (e.getTimezoneOffset() - t.getTimezoneOffset()) * Kt) /
              Xt,
            (t) => t.getDate() - 1,
          )),
        fe =
          (se.range,
          re(
            (t) => {
              t.setUTCHours(0, 0, 0, 0);
            },
            (t, e) => {
              t.setUTCDate(t.getUTCDate() + e);
            },
            (t, e) => (e - t) / Xt,
            (t) => t.getUTCDate() - 1,
          )),
        pe =
          (fe.range,
          re(
            (t) => {
              t.setUTCHours(0, 0, 0, 0);
            },
            (t, e) => {
              t.setUTCDate(t.getUTCDate() + e);
            },
            (t, e) => (e - t) / Xt,
            (t) => Math.floor(t / Xt),
          ));
      pe.range;
      function de(t) {
        return re(
          (e) => {
            e.setDate(e.getDate() - ((e.getDay() + 7 - t) % 7)),
              e.setHours(0, 0, 0, 0);
          },
          (t, e) => {
            t.setDate(t.getDate() + 7 * e);
          },
          (t, e) =>
            (e - t - (e.getTimezoneOffset() - t.getTimezoneOffset()) * Kt) / Qt,
        );
      }
      const he = de(0),
        ve = de(1),
        ye = de(2),
        me = de(3),
        ge = de(4),
        be = de(5),
        xe = de(6);
      he.range, ve.range, ye.range, me.range, ge.range, be.range, xe.range;
      function Oe(t) {
        return re(
          (e) => {
            e.setUTCDate(e.getUTCDate() - ((e.getUTCDay() + 7 - t) % 7)),
              e.setUTCHours(0, 0, 0, 0);
          },
          (t, e) => {
            t.setUTCDate(t.getUTCDate() + 7 * e);
          },
          (t, e) => (e - t) / Qt,
        );
      }
      const we = Oe(0),
        Ce = Oe(1),
        Se = Oe(2),
        Ae = Oe(3),
        je = Oe(4),
        ke = Oe(5),
        Pe = Oe(6),
        Ee =
          (we.range,
          Ce.range,
          Se.range,
          Ae.range,
          je.range,
          ke.range,
          Pe.range,
          re(
            (t) => {
              t.setDate(1), t.setHours(0, 0, 0, 0);
            },
            (t, e) => {
              t.setMonth(t.getMonth() + e);
            },
            (t, e) =>
              e.getMonth() -
              t.getMonth() +
              12 * (e.getFullYear() - t.getFullYear()),
            (t) => t.getMonth(),
          )),
        Me =
          (Ee.range,
          re(
            (t) => {
              t.setUTCDate(1), t.setUTCHours(0, 0, 0, 0);
            },
            (t, e) => {
              t.setUTCMonth(t.getUTCMonth() + e);
            },
            (t, e) =>
              e.getUTCMonth() -
              t.getUTCMonth() +
              12 * (e.getUTCFullYear() - t.getUTCFullYear()),
            (t) => t.getUTCMonth(),
          )),
        Te =
          (Me.range,
          re(
            (t) => {
              t.setMonth(0, 1), t.setHours(0, 0, 0, 0);
            },
            (t, e) => {
              t.setFullYear(t.getFullYear() + e);
            },
            (t, e) => e.getFullYear() - t.getFullYear(),
            (t) => t.getFullYear(),
          ));
      Te.every = (t) =>
        isFinite((t = Math.floor(t))) && t > 0
          ? re(
              (e) => {
                e.setFullYear(Math.floor(e.getFullYear() / t) * t),
                  e.setMonth(0, 1),
                  e.setHours(0, 0, 0, 0);
              },
              (e, n) => {
                e.setFullYear(e.getFullYear() + n * t);
              },
            )
          : null;
      Te.range;
      const _e = re(
        (t) => {
          t.setUTCMonth(0, 1), t.setUTCHours(0, 0, 0, 0);
        },
        (t, e) => {
          t.setUTCFullYear(t.getUTCFullYear() + e);
        },
        (t, e) => e.getUTCFullYear() - t.getUTCFullYear(),
        (t) => t.getUTCFullYear(),
      );
      _e.every = (t) =>
        isFinite((t = Math.floor(t))) && t > 0
          ? re(
              (e) => {
                e.setUTCFullYear(Math.floor(e.getUTCFullYear() / t) * t),
                  e.setUTCMonth(0, 1),
                  e.setUTCHours(0, 0, 0, 0);
              },
              (e, n) => {
                e.setUTCFullYear(e.getUTCFullYear() + n * t);
              },
            )
          : null;
      _e.range;
      function Le(t, e, n, r, o, a) {
        const i = [
          [ae, 1, Zt],
          [ae, 5, 5e3],
          [ae, 15, 15e3],
          [ae, 30, 3e4],
          [a, 1, Kt],
          [a, 5, 3e5],
          [a, 15, 9e5],
          [a, 30, 18e5],
          [o, 1, Gt],
          [o, 3, 108e5],
          [o, 6, 216e5],
          [o, 12, 432e5],
          [r, 1, Xt],
          [r, 2, 1728e5],
          [n, 1, Qt],
          [e, 1, Jt],
          [e, 3, 7776e6],
          [t, 1, te],
        ];
        function c(e, n, r) {
          const o = Math.abs(n - e) / r,
            a = L((t) => {
              let [, , e] = t;
              return e;
            }).right(i, o);
          if (a === i.length) return t.every(M(e / te, n / te, r));
          if (0 === a) return oe.every(Math.max(M(e, n, r), 1));
          const [c, l] = i[o / i[a - 1][2] < i[a][2] / o ? a - 1 : a];
          return c.every(l);
        }
        return [
          function (t, e, n) {
            const r = e < t;
            r && ([t, e] = [e, t]);
            const o = n && "function" === typeof n.range ? n : c(t, e, n),
              a = o ? o.range(t, +e + 1) : [];
            return r ? a.reverse() : a;
          },
          c,
        ];
      }
      const [De, Ie] = Le(_e, Me, we, pe, ue, ce),
        [Re, Ne] = Le(Te, Ee, he, se, le, ie);
      function We(t) {
        if (0 <= t.y && t.y < 100) {
          var e = new Date(-1, t.m, t.d, t.H, t.M, t.S, t.L);
          return e.setFullYear(t.y), e;
        }
        return new Date(t.y, t.m, t.d, t.H, t.M, t.S, t.L);
      }
      function Fe(t) {
        if (0 <= t.y && t.y < 100) {
          var e = new Date(Date.UTC(-1, t.m, t.d, t.H, t.M, t.S, t.L));
          return e.setUTCFullYear(t.y), e;
        }
        return new Date(Date.UTC(t.y, t.m, t.d, t.H, t.M, t.S, t.L));
      }
      function ze(t, e, n) {
        return { y: t, m: e, d: n, H: 0, M: 0, S: 0, L: 0 };
      }
      var Ue,
        Be,
        qe,
        He = { "-": "", _: " ", 0: "0" },
        Ve = /^\s*\d+/,
        $e = /^%/,
        Ye = /[\\^$*+?|[\]().{}]/g;
      function Ze(t, e, n) {
        var r = t < 0 ? "-" : "",
          o = (r ? -t : t) + "",
          a = o.length;
        return r + (a < n ? new Array(n - a + 1).join(e) + o : o);
      }
      function Ke(t) {
        return t.replace(Ye, "\\$&");
      }
      function Ge(t) {
        return new RegExp("^(?:" + t.map(Ke).join("|") + ")", "i");
      }
      function Xe(t) {
        return new Map(t.map((t, e) => [t.toLowerCase(), e]));
      }
      function Qe(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 1));
        return r ? ((t.w = +r[0]), n + r[0].length) : -1;
      }
      function Je(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 1));
        return r ? ((t.u = +r[0]), n + r[0].length) : -1;
      }
      function tn(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 2));
        return r ? ((t.U = +r[0]), n + r[0].length) : -1;
      }
      function en(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 2));
        return r ? ((t.V = +r[0]), n + r[0].length) : -1;
      }
      function nn(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 2));
        return r ? ((t.W = +r[0]), n + r[0].length) : -1;
      }
      function rn(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 4));
        return r ? ((t.y = +r[0]), n + r[0].length) : -1;
      }
      function on(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 2));
        return r
          ? ((t.y = +r[0] + (+r[0] > 68 ? 1900 : 2e3)), n + r[0].length)
          : -1;
      }
      function an(t, e, n) {
        var r = /^(Z)|([+-]\d\d)(?::?(\d\d))?/.exec(e.slice(n, n + 6));
        return r
          ? ((t.Z = r[1] ? 0 : -(r[2] + (r[3] || "00"))), n + r[0].length)
          : -1;
      }
      function cn(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 1));
        return r ? ((t.q = 3 * r[0] - 3), n + r[0].length) : -1;
      }
      function ln(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 2));
        return r ? ((t.m = r[0] - 1), n + r[0].length) : -1;
      }
      function un(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 2));
        return r ? ((t.d = +r[0]), n + r[0].length) : -1;
      }
      function sn(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 3));
        return r ? ((t.m = 0), (t.d = +r[0]), n + r[0].length) : -1;
      }
      function fn(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 2));
        return r ? ((t.H = +r[0]), n + r[0].length) : -1;
      }
      function pn(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 2));
        return r ? ((t.M = +r[0]), n + r[0].length) : -1;
      }
      function dn(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 2));
        return r ? ((t.S = +r[0]), n + r[0].length) : -1;
      }
      function hn(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 3));
        return r ? ((t.L = +r[0]), n + r[0].length) : -1;
      }
      function vn(t, e, n) {
        var r = Ve.exec(e.slice(n, n + 6));
        return r ? ((t.L = Math.floor(r[0] / 1e3)), n + r[0].length) : -1;
      }
      function yn(t, e, n) {
        var r = $e.exec(e.slice(n, n + 1));
        return r ? n + r[0].length : -1;
      }
      function mn(t, e, n) {
        var r = Ve.exec(e.slice(n));
        return r ? ((t.Q = +r[0]), n + r[0].length) : -1;
      }
      function gn(t, e, n) {
        var r = Ve.exec(e.slice(n));
        return r ? ((t.s = +r[0]), n + r[0].length) : -1;
      }
      function bn(t, e) {
        return Ze(t.getDate(), e, 2);
      }
      function xn(t, e) {
        return Ze(t.getHours(), e, 2);
      }
      function On(t, e) {
        return Ze(t.getHours() % 12 || 12, e, 2);
      }
      function wn(t, e) {
        return Ze(1 + se.count(Te(t), t), e, 3);
      }
      function Cn(t, e) {
        return Ze(t.getMilliseconds(), e, 3);
      }
      function Sn(t, e) {
        return Cn(t, e) + "000";
      }
      function An(t, e) {
        return Ze(t.getMonth() + 1, e, 2);
      }
      function jn(t, e) {
        return Ze(t.getMinutes(), e, 2);
      }
      function kn(t, e) {
        return Ze(t.getSeconds(), e, 2);
      }
      function Pn(t) {
        var e = t.getDay();
        return 0 === e ? 7 : e;
      }
      function En(t, e) {
        return Ze(he.count(Te(t) - 1, t), e, 2);
      }
      function Mn(t) {
        var e = t.getDay();
        return e >= 4 || 0 === e ? ge(t) : ge.ceil(t);
      }
      function Tn(t, e) {
        return (
          (t = Mn(t)), Ze(ge.count(Te(t), t) + (4 === Te(t).getDay()), e, 2)
        );
      }
      function _n(t) {
        return t.getDay();
      }
      function Ln(t, e) {
        return Ze(ve.count(Te(t) - 1, t), e, 2);
      }
      function Dn(t, e) {
        return Ze(t.getFullYear() % 100, e, 2);
      }
      function In(t, e) {
        return Ze((t = Mn(t)).getFullYear() % 100, e, 2);
      }
      function Rn(t, e) {
        return Ze(t.getFullYear() % 1e4, e, 4);
      }
      function Nn(t, e) {
        var n = t.getDay();
        return Ze(
          (t = n >= 4 || 0 === n ? ge(t) : ge.ceil(t)).getFullYear() % 1e4,
          e,
          4,
        );
      }
      function Wn(t) {
        var e = t.getTimezoneOffset();
        return (
          (e > 0 ? "-" : ((e *= -1), "+")) +
          Ze((e / 60) | 0, "0", 2) +
          Ze(e % 60, "0", 2)
        );
      }
      function Fn(t, e) {
        return Ze(t.getUTCDate(), e, 2);
      }
      function zn(t, e) {
        return Ze(t.getUTCHours(), e, 2);
      }
      function Un(t, e) {
        return Ze(t.getUTCHours() % 12 || 12, e, 2);
      }
      function Bn(t, e) {
        return Ze(1 + fe.count(_e(t), t), e, 3);
      }
      function qn(t, e) {
        return Ze(t.getUTCMilliseconds(), e, 3);
      }
      function Hn(t, e) {
        return qn(t, e) + "000";
      }
      function Vn(t, e) {
        return Ze(t.getUTCMonth() + 1, e, 2);
      }
      function $n(t, e) {
        return Ze(t.getUTCMinutes(), e, 2);
      }
      function Yn(t, e) {
        return Ze(t.getUTCSeconds(), e, 2);
      }
      function Zn(t) {
        var e = t.getUTCDay();
        return 0 === e ? 7 : e;
      }
      function Kn(t, e) {
        return Ze(we.count(_e(t) - 1, t), e, 2);
      }
      function Gn(t) {
        var e = t.getUTCDay();
        return e >= 4 || 0 === e ? je(t) : je.ceil(t);
      }
      function Xn(t, e) {
        return (
          (t = Gn(t)), Ze(je.count(_e(t), t) + (4 === _e(t).getUTCDay()), e, 2)
        );
      }
      function Qn(t) {
        return t.getUTCDay();
      }
      function Jn(t, e) {
        return Ze(Ce.count(_e(t) - 1, t), e, 2);
      }
      function tr(t, e) {
        return Ze(t.getUTCFullYear() % 100, e, 2);
      }
      function er(t, e) {
        return Ze((t = Gn(t)).getUTCFullYear() % 100, e, 2);
      }
      function nr(t, e) {
        return Ze(t.getUTCFullYear() % 1e4, e, 4);
      }
      function rr(t, e) {
        var n = t.getUTCDay();
        return Ze(
          (t = n >= 4 || 0 === n ? je(t) : je.ceil(t)).getUTCFullYear() % 1e4,
          e,
          4,
        );
      }
      function or() {
        return "+0000";
      }
      function ar() {
        return "%";
      }
      function ir(t) {
        return +t;
      }
      function cr(t) {
        return Math.floor(+t / 1e3);
      }
      function lr(t) {
        return new Date(t);
      }
      function ur(t) {
        return t instanceof Date ? +t : +new Date(+t);
      }
      function sr(t, e, n, r, o, a, i, c, l, u) {
        var s = G(),
          f = s.invert,
          p = s.domain,
          d = u(".%L"),
          h = u(":%S"),
          v = u("%I:%M"),
          y = u("%I %p"),
          m = u("%a %d"),
          g = u("%b %d"),
          b = u("%B"),
          x = u("%Y");
        function O(t) {
          return (
            l(t) < t
              ? d
              : c(t) < t
                ? h
                : i(t) < t
                  ? v
                  : a(t) < t
                    ? y
                    : r(t) < t
                      ? o(t) < t
                        ? m
                        : g
                      : n(t) < t
                        ? b
                        : x
          )(t);
        }
        return (
          (s.invert = function (t) {
            return new Date(f(t));
          }),
          (s.domain = function (t) {
            return arguments.length ? p(Array.from(t, ur)) : p().map(lr);
          }),
          (s.ticks = function (e) {
            var n = p();
            return t(n[0], n[n.length - 1], null == e ? 10 : e);
          }),
          (s.tickFormat = function (t, e) {
            return null == e ? O : u(e);
          }),
          (s.nice = function (t) {
            var n = p();
            return (
              (t && "function" === typeof t.range) ||
                (t = e(n[0], n[n.length - 1], null == t ? 10 : t)),
              t ? p(yt(n, t)) : s
            );
          }),
          (s.copy = function () {
            return Z(s, sr(t, e, n, r, o, a, i, c, l, u));
          }),
          s
        );
      }
      function fr() {
        return p.apply(
          sr(Re, Ne, Te, Ee, he, se, le, ie, ae, Be).domain([
            new Date(2e3, 0, 1),
            new Date(2e3, 0, 2),
          ]),
          arguments,
        );
      }
      function pr() {
        return p.apply(
          sr(De, Ie, _e, Me, we, fe, ue, ce, ae, qe).domain([
            Date.UTC(2e3, 0, 1),
            Date.UTC(2e3, 0, 2),
          ]),
          arguments,
        );
      }
      function dr() {
        var t,
          e,
          n,
          r,
          o,
          a = 0,
          i = 1,
          c = H,
          l = !1;
        function u(e) {
          return null == e || isNaN((e = +e))
            ? o
            : c(
                0 === n
                  ? 0.5
                  : ((e = (r(e) - t) * n), l ? Math.max(0, Math.min(1, e)) : e),
              );
        }
        function s(t) {
          return function (e) {
            var n, r;
            return arguments.length
              ? (([n, r] = e), (c = t(n, r)), u)
              : [c(0), c(1)];
          };
        }
        return (
          (u.domain = function (o) {
            return arguments.length
              ? (([a, i] = o),
                (t = r((a = +a))),
                (e = r((i = +i))),
                (n = t === e ? 0 : 1 / (e - t)),
                u)
              : [a, i];
          }),
          (u.clamp = function (t) {
            return arguments.length ? ((l = !!t), u) : l;
          }),
          (u.interpolator = function (t) {
            return arguments.length ? ((c = t), u) : c;
          }),
          (u.range = s(F.Z)),
          (u.rangeRound = s(U)),
          (u.unknown = function (t) {
            return arguments.length ? ((o = t), u) : o;
          }),
          function (o) {
            return (
              (r = o),
              (t = o(a)),
              (e = o(i)),
              (n = t === e ? 0 : 1 / (e - t)),
              u
            );
          }
        );
      }
      function hr(t, e) {
        return e
          .domain(t.domain())
          .interpolator(t.interpolator())
          .clamp(t.clamp())
          .unknown(t.unknown());
      }
      function vr() {
        var t = dt(dr()(H));
        return (
          (t.copy = function () {
            return hr(t, vr());
          }),
          d.apply(t, arguments)
        );
      }
      function yr() {
        var t = Ct(dr()).domain([1, 10]);
        return (
          (t.copy = function () {
            return hr(t, yr()).base(t.base());
          }),
          d.apply(t, arguments)
        );
      }
      function mr() {
        var t = kt(dr());
        return (
          (t.copy = function () {
            return hr(t, mr()).constant(t.constant());
          }),
          d.apply(t, arguments)
        );
      }
      function gr() {
        var t = _t(dr());
        return (
          (t.copy = function () {
            return hr(t, gr()).exponent(t.exponent());
          }),
          d.apply(t, arguments)
        );
      }
      function br() {
        return gr.apply(null, arguments).exponent(0.5);
      }
      function xr() {
        var t = [],
          e = H;
        function n(n) {
          if (null != n && !isNaN((n = +n)))
            return e((W(t, n, 1) - 1) / (t.length - 1));
        }
        return (
          (n.domain = function (e) {
            if (!arguments.length) return t.slice();
            t = [];
            for (let n of e) null == n || isNaN((n = +n)) || t.push(n);
            return t.sort(T), n;
          }),
          (n.interpolator = function (t) {
            return arguments.length ? ((e = t), n) : e;
          }),
          (n.range = function () {
            return t.map((n, r) => e(r / (t.length - 1)));
          }),
          (n.quantiles = function (e) {
            return Array.from({ length: e + 1 }, (n, r) => qt(t, r / e));
          }),
          (n.copy = function () {
            return xr(e).domain(t);
          }),
          d.apply(n, arguments)
        );
      }
      function Or() {
        var t,
          e,
          n,
          r,
          o,
          a,
          i,
          c = 0,
          l = 0.5,
          u = 1,
          s = 1,
          f = H,
          p = !1;
        function d(t) {
          return isNaN((t = +t))
            ? i
            : ((t = 0.5 + ((t = +a(t)) - e) * (s * t < s * e ? r : o)),
              f(p ? Math.max(0, Math.min(1, t)) : t));
        }
        function h(t) {
          return function (e) {
            var n, r, o;
            return arguments.length
              ? (([n, r, o] = e),
                (f = (function (t, e) {
                  void 0 === e && ((e = t), (t = F.Z));
                  for (
                    var n = 0,
                      r = e.length - 1,
                      o = e[0],
                      a = new Array(r < 0 ? 0 : r);
                    n < r;

                  )
                    a[n] = t(o, (o = e[++n]));
                  return function (t) {
                    var e = Math.max(0, Math.min(r - 1, Math.floor((t *= r))));
                    return a[e](t - e);
                  };
                })(t, [n, r, o])),
                d)
              : [f(0), f(0.5), f(1)];
          };
        }
        return (
          (d.domain = function (i) {
            return arguments.length
              ? (([c, l, u] = i),
                (t = a((c = +c))),
                (e = a((l = +l))),
                (n = a((u = +u))),
                (r = t === e ? 0 : 0.5 / (e - t)),
                (o = e === n ? 0 : 0.5 / (n - e)),
                (s = e < t ? -1 : 1),
                d)
              : [c, l, u];
          }),
          (d.clamp = function (t) {
            return arguments.length ? ((p = !!t), d) : p;
          }),
          (d.interpolator = function (t) {
            return arguments.length ? ((f = t), d) : f;
          }),
          (d.range = h(F.Z)),
          (d.rangeRound = h(U)),
          (d.unknown = function (t) {
            return arguments.length ? ((i = t), d) : i;
          }),
          function (i) {
            return (
              (a = i),
              (t = i(c)),
              (e = i(l)),
              (n = i(u)),
              (r = t === e ? 0 : 0.5 / (e - t)),
              (o = e === n ? 0 : 0.5 / (n - e)),
              (s = e < t ? -1 : 1),
              d
            );
          }
        );
      }
      function wr() {
        var t = dt(Or()(H));
        return (
          (t.copy = function () {
            return hr(t, wr());
          }),
          d.apply(t, arguments)
        );
      }
      function Cr() {
        var t = Ct(Or()).domain([0.1, 1, 10]);
        return (
          (t.copy = function () {
            return hr(t, Cr()).base(t.base());
          }),
          d.apply(t, arguments)
        );
      }
      function Sr() {
        var t = kt(Or());
        return (
          (t.copy = function () {
            return hr(t, Sr()).constant(t.constant());
          }),
          d.apply(t, arguments)
        );
      }
      function Ar() {
        var t = _t(Or());
        return (
          (t.copy = function () {
            return hr(t, Ar()).exponent(t.exponent());
          }),
          d.apply(t, arguments)
        );
      }
      function jr() {
        return Ar.apply(null, arguments).exponent(0.5);
      }
      !(function (t) {
        (Ue = (function (t) {
          var e = t.dateTime,
            n = t.date,
            r = t.time,
            o = t.periods,
            a = t.days,
            i = t.shortDays,
            c = t.months,
            l = t.shortMonths,
            u = Ge(o),
            s = Xe(o),
            f = Ge(a),
            p = Xe(a),
            d = Ge(i),
            h = Xe(i),
            v = Ge(c),
            y = Xe(c),
            m = Ge(l),
            g = Xe(l),
            b = {
              a: function (t) {
                return i[t.getDay()];
              },
              A: function (t) {
                return a[t.getDay()];
              },
              b: function (t) {
                return l[t.getMonth()];
              },
              B: function (t) {
                return c[t.getMonth()];
              },
              c: null,
              d: bn,
              e: bn,
              f: Sn,
              g: In,
              G: Nn,
              H: xn,
              I: On,
              j: wn,
              L: Cn,
              m: An,
              M: jn,
              p: function (t) {
                return o[+(t.getHours() >= 12)];
              },
              q: function (t) {
                return 1 + ~~(t.getMonth() / 3);
              },
              Q: ir,
              s: cr,
              S: kn,
              u: Pn,
              U: En,
              V: Tn,
              w: _n,
              W: Ln,
              x: null,
              X: null,
              y: Dn,
              Y: Rn,
              Z: Wn,
              "%": ar,
            },
            x = {
              a: function (t) {
                return i[t.getUTCDay()];
              },
              A: function (t) {
                return a[t.getUTCDay()];
              },
              b: function (t) {
                return l[t.getUTCMonth()];
              },
              B: function (t) {
                return c[t.getUTCMonth()];
              },
              c: null,
              d: Fn,
              e: Fn,
              f: Hn,
              g: er,
              G: rr,
              H: zn,
              I: Un,
              j: Bn,
              L: qn,
              m: Vn,
              M: $n,
              p: function (t) {
                return o[+(t.getUTCHours() >= 12)];
              },
              q: function (t) {
                return 1 + ~~(t.getUTCMonth() / 3);
              },
              Q: ir,
              s: cr,
              S: Yn,
              u: Zn,
              U: Kn,
              V: Xn,
              w: Qn,
              W: Jn,
              x: null,
              X: null,
              y: tr,
              Y: nr,
              Z: or,
              "%": ar,
            },
            O = {
              a: function (t, e, n) {
                var r = d.exec(e.slice(n));
                return r
                  ? ((t.w = h.get(r[0].toLowerCase())), n + r[0].length)
                  : -1;
              },
              A: function (t, e, n) {
                var r = f.exec(e.slice(n));
                return r
                  ? ((t.w = p.get(r[0].toLowerCase())), n + r[0].length)
                  : -1;
              },
              b: function (t, e, n) {
                var r = m.exec(e.slice(n));
                return r
                  ? ((t.m = g.get(r[0].toLowerCase())), n + r[0].length)
                  : -1;
              },
              B: function (t, e, n) {
                var r = v.exec(e.slice(n));
                return r
                  ? ((t.m = y.get(r[0].toLowerCase())), n + r[0].length)
                  : -1;
              },
              c: function (t, n, r) {
                return S(t, e, n, r);
              },
              d: un,
              e: un,
              f: vn,
              g: on,
              G: rn,
              H: fn,
              I: fn,
              j: sn,
              L: hn,
              m: ln,
              M: pn,
              p: function (t, e, n) {
                var r = u.exec(e.slice(n));
                return r
                  ? ((t.p = s.get(r[0].toLowerCase())), n + r[0].length)
                  : -1;
              },
              q: cn,
              Q: mn,
              s: gn,
              S: dn,
              u: Je,
              U: tn,
              V: en,
              w: Qe,
              W: nn,
              x: function (t, e, r) {
                return S(t, n, e, r);
              },
              X: function (t, e, n) {
                return S(t, r, e, n);
              },
              y: on,
              Y: rn,
              Z: an,
              "%": yn,
            };
          function w(t, e) {
            return function (n) {
              var r,
                o,
                a,
                i = [],
                c = -1,
                l = 0,
                u = t.length;
              for (n instanceof Date || (n = new Date(+n)); ++c < u; )
                37 === t.charCodeAt(c) &&
                  (i.push(t.slice(l, c)),
                  null != (o = He[(r = t.charAt(++c))])
                    ? (r = t.charAt(++c))
                    : (o = "e" === r ? " " : "0"),
                  (a = e[r]) && (r = a(n, o)),
                  i.push(r),
                  (l = c + 1));
              return i.push(t.slice(l, c)), i.join("");
            };
          }
          function C(t, e) {
            return function (n) {
              var r,
                o,
                a = ze(1900, void 0, 1);
              if (S(a, t, (n += ""), 0) != n.length) return null;
              if ("Q" in a) return new Date(a.Q);
              if ("s" in a) return new Date(1e3 * a.s + ("L" in a ? a.L : 0));
              if (
                (e && !("Z" in a) && (a.Z = 0),
                "p" in a && (a.H = (a.H % 12) + 12 * a.p),
                void 0 === a.m && (a.m = "q" in a ? a.q : 0),
                "V" in a)
              ) {
                if (a.V < 1 || a.V > 53) return null;
                "w" in a || (a.w = 1),
                  "Z" in a
                    ? ((o = (r = Fe(ze(a.y, 0, 1))).getUTCDay()),
                      (r = o > 4 || 0 === o ? Ce.ceil(r) : Ce(r)),
                      (r = fe.offset(r, 7 * (a.V - 1))),
                      (a.y = r.getUTCFullYear()),
                      (a.m = r.getUTCMonth()),
                      (a.d = r.getUTCDate() + ((a.w + 6) % 7)))
                    : ((o = (r = We(ze(a.y, 0, 1))).getDay()),
                      (r = o > 4 || 0 === o ? ve.ceil(r) : ve(r)),
                      (r = se.offset(r, 7 * (a.V - 1))),
                      (a.y = r.getFullYear()),
                      (a.m = r.getMonth()),
                      (a.d = r.getDate() + ((a.w + 6) % 7)));
              } else
                ("W" in a || "U" in a) &&
                  ("w" in a || (a.w = "u" in a ? a.u % 7 : "W" in a ? 1 : 0),
                  (o =
                    "Z" in a
                      ? Fe(ze(a.y, 0, 1)).getUTCDay()
                      : We(ze(a.y, 0, 1)).getDay()),
                  (a.m = 0),
                  (a.d =
                    "W" in a
                      ? ((a.w + 6) % 7) + 7 * a.W - ((o + 5) % 7)
                      : a.w + 7 * a.U - ((o + 6) % 7)));
              return "Z" in a
                ? ((a.H += (a.Z / 100) | 0), (a.M += a.Z % 100), Fe(a))
                : We(a);
            };
          }
          function S(t, e, n, r) {
            for (var o, a, i = 0, c = e.length, l = n.length; i < c; ) {
              if (r >= l) return -1;
              if (37 === (o = e.charCodeAt(i++))) {
                if (
                  ((o = e.charAt(i++)),
                  !(a = O[o in He ? e.charAt(i++) : o]) || (r = a(t, n, r)) < 0)
                )
                  return -1;
              } else if (o != n.charCodeAt(r++)) return -1;
            }
            return r;
          }
          return (
            (b.x = w(n, b)),
            (b.X = w(r, b)),
            (b.c = w(e, b)),
            (x.x = w(n, x)),
            (x.X = w(r, x)),
            (x.c = w(e, x)),
            {
              format: function (t) {
                var e = w((t += ""), b);
                return (
                  (e.toString = function () {
                    return t;
                  }),
                  e
                );
              },
              parse: function (t) {
                var e = C((t += ""), !1);
                return (
                  (e.toString = function () {
                    return t;
                  }),
                  e
                );
              },
              utcFormat: function (t) {
                var e = w((t += ""), x);
                return (
                  (e.toString = function () {
                    return t;
                  }),
                  e
                );
              },
              utcParse: function (t) {
                var e = C((t += ""), !0);
                return (
                  (e.toString = function () {
                    return t;
                  }),
                  e
                );
              },
            }
          );
        })(t)),
          (Be = Ue.format),
          Ue.parse,
          (qe = Ue.utcFormat),
          Ue.utcParse;
      })({
        dateTime: "%x, %X",
        date: "%-m/%-d/%Y",
        time: "%-I:%M:%S %p",
        periods: ["AM", "PM"],
        days: [
          "Sunday",
          "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday",
          "Saturday",
        ],
        shortDays: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        months: [
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December",
        ],
        shortMonths: [
          "Jan",
          "Feb",
          "Mar",
          "Apr",
          "May",
          "Jun",
          "Jul",
          "Aug",
          "Sep",
          "Oct",
          "Nov",
          "Dec",
        ],
      });
      var kr = ["linear", "time", "log", "sqrt"];
      function Pr(t) {
        return "function" === typeof t
          ? c()(t.copy) && c()(t.domain) && c()(t.range)
          : "string" === typeof t && u()(kr, t);
      }
      function Er(t, e) {
        return !!t.scale && ((!t.scale.x && !t.scale.y) || !!t.scale[e]);
      }
      function Mr(t, e) {
        if (!t.data) return "linear";
        var n = s.$0(t[e]),
          r = t.data.map(function (t) {
            var r = a()(n(t)) ? n(t)[e] : n(t);
            return void 0 !== r ? r : t[e];
          });
        return f.AM(r) ? "time" : "linear";
      }
      function Tr(t) {
        if (Pr(t)) {
          var e = (function (t) {
            var e;
            return "scale".concat((e = t) && e[0].toUpperCase() + e.slice(1));
          })(t);
          return r[e]();
        }
        return ht();
      }
      function _r(t, e) {
        var n = Lr(t, e);
        return n
          ? "string" === typeof n
            ? Tr(n)
            : n
          : Tr(
              (function (t, e) {
                var n;
                if (
                  (t.domain && t.domain[e]
                    ? (n = t.domain[e])
                    : t.domain && Array.isArray(t.domain) && (n = t.domain),
                  n)
                )
                  return f.AM(n) ? "time" : "linear";
              })(t, e) || Mr(t, e),
            );
      }
      function Lr(t, e) {
        if (Er(t, e)) {
          var n = t.scale[e] || t.scale;
          return Pr(n) ? (c()(n) ? n : Tr(n)) : void 0;
        }
      }
      function Dr(t, e) {
        return (
          (function (t, e) {
            if (Er(t, e)) {
              var n = t.scale[e] || t.scale;
              return "string" === typeof n ? n : Rr(n);
            }
          })(t, e) || Mr(t, e)
        );
      }
      var Ir = [
        { name: "quantile", method: "quantiles" },
        { name: "log", method: "base" },
      ];
      function Rr(t) {
        if ("string" === typeof t) return t;
        var e = Ir.filter(function (e) {
          return void 0 !== t[e.method];
        })[0];
        return e ? e.name : void 0;
      }
    },
    30637: (t, e, n) => {
      "use strict";
      n.d(e, { _: () => r, p: () => o });
      var r = function (t) {
        for (
          var e = arguments.length, n = new Array(e > 1 ? e - 1 : 0), o = 1;
          o < e;
          o++
        )
          n[o - 1] = arguments[o];
        if (n.length > 0)
          return n
            .reduce(function (t, e) {
              return [t, r(e)].join(" ");
            }, r(t))
            .trim();
        if (void 0 === t || null === t || "string" === typeof t) return t;
        var a = [];
        for (var i in t)
          if (t.hasOwnProperty(i)) {
            var c = t[i];
            a.push("".concat(i, "(").concat(c, ")"));
          }
        return a.join(" ").trim();
      };
      function o(t) {
        var e = {
          grayscale: ["#cccccc", "#969696", "#636363", "#252525"],
          qualitative: [
            "#334D5C",
            "#45B29D",
            "#EFC94C",
            "#E27A3F",
            "#DF5A49",
            "#4F7DA1",
            "#55DBC1",
            "#EFDA97",
            "#E2A37F",
            "#DF948A",
          ],
          heatmap: ["#428517", "#77D200", "#D6D305", "#EC8E19", "#C92B05"],
          warm: ["#940031", "#C43343", "#DC5429", "#FF821D", "#FFAF55"],
          cool: ["#2746B9", "#0B69D4", "#2794DB", "#31BB76", "#60E83B"],
          red: ["#FCAE91", "#FB6A4A", "#DE2D26", "#A50F15", "#750B0E"],
          blue: ["#002C61", "#004B8F", "#006BC9", "#3795E5", "#65B4F4"],
          green: ["#354722", "#466631", "#649146", "#8AB25C", "#A9C97E"],
        };
        return t ? e[t] : e.grayscale;
      }
    },
    62795: (t, e, n) => {
      "use strict";
      n.d(e, { Tj: () => O, Z9: () => E });
      var r = n(49151),
        o = n.n(r),
        a = n(66933),
        i = n.n(a),
        c = n(15687),
        l = n.n(c);
      function u(t, e) {
        return (
          (function (t) {
            if (Array.isArray(t)) return t;
          })(t) ||
          (function (t, e) {
            var n =
              null == t
                ? null
                : ("undefined" !== typeof Symbol && t[Symbol.iterator]) ||
                  t["@@iterator"];
            if (null == n) return;
            var r,
              o,
              a = [],
              i = !0,
              c = !1;
            try {
              for (
                n = n.call(t);
                !(i = (r = n.next()).done) &&
                (a.push(r.value), !e || a.length !== e);
                i = !0
              );
            } catch (l) {
              (c = !0), (o = l);
            } finally {
              try {
                i || null == n.return || n.return();
              } finally {
                if (c) throw o;
              }
            }
            return a;
          })(t, e) ||
          f(t, e) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function s(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return p(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          f(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function f(t, e) {
        if (t) {
          if ("string" === typeof t) return p(t, e);
          var n = Object.prototype.toString.call(t).slice(8, -1);
          return (
            "Object" === n && t.constructor && (n = t.constructor.name),
            "Map" === n || "Set" === n
              ? Array.from(t)
              : "Arguments" === n ||
                  /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
                ? p(t, e)
                : void 0
          );
        }
      }
      function p(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      var d = {
          "American Typewriter": {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0.4203125, 0.3296875, 0.6,
              0.6375, 0.8015625, 0.8203125, 0.1875, 0.45625, 0.45625, 0.6375,
              0.5, 0.2734375, 0.309375, 0.2734375, 0.4390625, 0.6375, 0.6375,
              0.6375, 0.6375, 0.6375, 0.6375, 0.6375, 0.6375, 0.6375, 0.6375,
              0.2734375, 0.2734375, 0.5, 0.5, 0.5, 0.6, 0.6921875, 0.7640625,
              0.6921875, 0.6375, 0.728125, 0.6734375, 0.6203125, 0.7109375,
              0.784375, 0.3828125, 0.6421875, 0.7859375, 0.6375, 0.9484375,
              0.7640625, 0.65625, 0.6375, 0.65625, 0.7296875, 0.6203125, 0.6375,
              0.7109375, 0.740625, 0.940625, 0.784375, 0.7578125, 0.6203125,
              0.4375, 0.5, 0.4375, 0.5, 0.5, 0.4921875, 0.5734375, 0.5890625,
              0.5109375, 0.6, 0.528125, 0.43125, 0.5578125, 0.6375, 0.3109375,
              0.40625, 0.6234375, 0.309375, 0.928125, 0.6375, 0.546875, 0.6,
              0.58125, 0.4921875, 0.4921875, 0.4, 0.6203125, 0.625, 0.825,
              0.6375, 0.640625, 0.528125, 0.5, 0.5, 0.5, 0.6671875,
            ],
            avg: 0.5793421052631578,
          },
          Arial: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.278125, 0.278125, 0.35625,
              0.55625, 0.55625, 0.890625, 0.6671875, 0.1921875, 0.334375,
              0.334375, 0.390625, 0.584375, 0.278125, 0.334375, 0.278125,
              0.278125, 0.55625, 0.55625, 0.55625, 0.55625, 0.55625, 0.55625,
              0.55625, 0.55625, 0.55625, 0.55625, 0.278125, 0.278125, 0.584375,
              0.584375, 0.584375, 0.55625, 1.015625, 0.6703125, 0.6671875,
              0.7234375, 0.7234375, 0.6671875, 0.6109375, 0.778125, 0.7234375,
              0.278125, 0.5, 0.6671875, 0.55625, 0.834375, 0.7234375, 0.778125,
              0.6671875, 0.778125, 0.7234375, 0.6671875, 0.6109375, 0.7234375,
              0.6671875, 0.9453125, 0.6671875, 0.6671875, 0.6109375, 0.278125,
              0.278125, 0.278125, 0.4703125, 0.584375, 0.334375, 0.55625,
              0.55625, 0.5, 0.55625, 0.55625, 0.3125, 0.55625, 0.55625,
              0.2234375, 0.2703125, 0.5, 0.2234375, 0.834375, 0.55625, 0.55625,
              0.55625, 0.55625, 0.346875, 0.5, 0.278125, 0.55625, 0.5,
              0.7234375, 0.5, 0.5, 0.5, 0.334375, 0.2609375, 0.334375, 0.584375,
            ],
            avg: 0.528733552631579,
          },
          "Arial Black": {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.33125, 0.334375, 0.5, 0.6609375,
              0.6671875, 1, 0.890625, 0.278125, 0.390625, 0.390625, 0.55625,
              0.6609375, 0.334375, 0.334375, 0.334375, 0.28125, 0.6671875,
              0.6671875, 0.6671875, 0.6671875, 0.6671875, 0.6671875, 0.6671875,
              0.6671875, 0.6671875, 0.6671875, 0.334375, 0.334375, 0.6609375,
              0.6609375, 0.6609375, 0.6109375, 0.7453125, 0.78125, 0.778125,
              0.778125, 0.778125, 0.7234375, 0.6671875, 0.834375, 0.834375,
              0.390625, 0.6671875, 0.834375, 0.6671875, 0.9453125, 0.834375,
              0.834375, 0.7234375, 0.834375, 0.78125, 0.7234375, 0.7234375,
              0.834375, 0.7796875, 1.003125, 0.78125, 0.78125, 0.7234375,
              0.390625, 0.28125, 0.390625, 0.6609375, 0.5125, 0.334375,
              0.6671875, 0.6671875, 0.6671875, 0.6671875, 0.6671875, 0.41875,
              0.6671875, 0.6671875, 0.334375, 0.384375, 0.6671875, 0.334375, 1,
              0.6671875, 0.6671875, 0.6671875, 0.6671875, 0.4703125, 0.6109375,
              0.4453125, 0.6671875, 0.6140625, 0.946875, 0.6671875, 0.615625,
              0.55625, 0.390625, 0.278125, 0.390625, 0.6609375,
            ],
            avg: 0.6213157894736842,
          },
          Baskerville: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0.25, 0.40625, 0.6671875,
              0.490625, 0.875, 0.7015625, 0.178125, 0.2453125, 0.246875,
              0.4171875, 0.6671875, 0.25, 0.3125, 0.25, 0.521875, 0.5, 0.5, 0.5,
              0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.6671875,
              0.6671875, 0.6671875, 0.396875, 0.9171875, 0.684375, 0.615625,
              0.71875, 0.7609375, 0.625, 0.553125, 0.771875, 0.803125,
              0.3546875, 0.515625, 0.78125, 0.6046875, 0.928125, 0.75,
              0.8234375, 0.5625, 0.96875, 0.7296875, 0.5421875, 0.6984375,
              0.771875, 0.7296875, 0.9484375, 0.771875, 0.678125, 0.6359375,
              0.3640625, 0.521875, 0.3640625, 0.46875, 0.5125, 0.334375,
              0.46875, 0.521875, 0.428125, 0.521875, 0.4375, 0.3890625,
              0.4765625, 0.53125, 0.25, 0.359375, 0.4640625, 0.240625, 0.803125,
              0.53125, 0.5, 0.521875, 0.521875, 0.365625, 0.334375, 0.2921875,
              0.521875, 0.4640625, 0.678125, 0.4796875, 0.465625, 0.428125,
              0.4796875, 0.5109375, 0.4796875, 0.6671875,
            ],
            avg: 0.5323519736842108,
          },
          Courier: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5984375, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6078125, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.61875, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.615625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6140625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625,
            ],
            avg: 0.6020559210526316,
          },
          "Courier New": {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5984375, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625,
            ],
            avg: 0.6015296052631579,
          },
          cursive: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1921875, 0.24375, 0.40625,
              0.5671875, 0.3984375, 0.721875, 0.909375, 0.2328125, 0.434375,
              0.365625, 0.4734375, 0.5578125, 0.19375, 0.3484375, 0.19375,
              0.7734375, 0.503125, 0.4171875, 0.5453125, 0.45, 0.6046875,
              0.4703125, 0.5984375, 0.55625, 0.503125, 0.5546875, 0.20625, 0.2,
              0.5625, 0.5546875, 0.546875, 0.403125, 0.70625, 0.734375,
              0.7078125, 0.64375, 0.85, 0.753125, 0.75, 0.6484375, 1.0765625,
              0.44375, 0.5359375, 0.8359375, 0.653125, 1.0109375, 1.1515625,
              0.6796875, 0.6984375, 1.0625, 0.8234375, 0.5125, 0.9234375,
              0.8546875, 0.70625, 0.9109375, 0.7421875, 0.715625, 0.6015625,
              0.4640625, 0.3359375, 0.4109375, 0.5421875, 0.5421875, 0.4328125,
              0.5125, 0.5, 0.3859375, 0.7375, 0.359375, 0.75625, 0.540625,
              0.5328125, 0.3203125, 0.5296875, 0.5015625, 0.484375, 0.7890625,
              0.5640625, 0.4203125, 0.703125, 0.471875, 0.4734375, 0.35, 0.4125,
              0.5640625, 0.471875, 0.6484375, 0.5296875, 0.575, 0.4140625,
              0.415625, 0.20625, 0.3796875, 0.5421875,
            ],
            avg: 0.5604440789473684,
          },
          fantasy: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.215625, 0.2625, 0.3265625,
              0.6109375, 0.534375, 0.7625, 0.7828125, 0.2, 0.4359375, 0.4359375,
              0.3765625, 0.5109375, 0.2796875, 0.4609375, 0.2796875, 0.5296875,
              0.6640625, 0.253125, 0.521875, 0.4765625, 0.6640625, 0.490625,
              0.528125, 0.5546875, 0.496875, 0.5421875, 0.2796875, 0.2796875,
              0.5625, 0.4609375, 0.5625, 0.4828125, 0.609375, 0.740625,
              0.7234375, 0.740625, 0.8265625, 0.7234375, 0.6171875, 0.7359375,
              0.765625, 0.240625, 0.5453125, 0.715625, 0.6078125, 0.8640625,
              0.653125, 0.9125, 0.6484375, 0.946875, 0.6921875, 0.653125,
              0.6953125, 0.8015625, 0.58125, 0.784375, 0.671875, 0.6265625,
              0.690625, 0.4359375, 0.5296875, 0.4359375, 0.53125, 0.5, 0.2875,
              0.5375, 0.603125, 0.4984375, 0.60625, 0.53125, 0.434375,
              0.6421875, 0.56875, 0.209375, 0.4671875, 0.5484375, 0.2203125,
              0.709375, 0.55, 0.5984375, 0.6140625, 0.5765625, 0.40625,
              0.4734375, 0.3734375, 0.559375, 0.4421875, 0.6421875, 0.4890625,
              0.578125, 0.4484375, 0.2546875, 0.2203125, 0.2546875, 0.55,
            ],
            avg: 0.536496710526316,
          },
          Geneva: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.3328125, 0.3046875, 0.5,
              0.6671875, 0.6671875, 0.90625, 0.728125, 0.3046875, 0.446875,
              0.446875, 0.5078125, 0.6671875, 0.3046875, 0.3796875, 0.3046875,
              0.5390625, 0.6671875, 0.6671875, 0.6671875, 0.6671875, 0.6671875,
              0.6671875, 0.6671875, 0.6671875, 0.6671875, 0.6671875, 0.3046875,
              0.3046875, 0.6671875, 0.6671875, 0.6671875, 0.56875, 0.871875,
              0.728125, 0.6375, 0.6515625, 0.7015625, 0.5765625, 0.5546875,
              0.675, 0.690625, 0.2421875, 0.4921875, 0.6640625, 0.584375,
              0.7890625, 0.709375, 0.7359375, 0.584375, 0.78125, 0.60625,
              0.60625, 0.640625, 0.6671875, 0.728125, 0.946875, 0.6109375,
              0.6109375, 0.5765625, 0.446875, 0.5390625, 0.446875, 0.6671875,
              0.6671875, 0.5921875, 0.5546875, 0.6109375, 0.546875, 0.603125,
              0.5765625, 0.390625, 0.6109375, 0.584375, 0.2359375, 0.334375,
              0.5390625, 0.2359375, 0.8953125, 0.584375, 0.60625, 0.603125,
              0.603125, 0.3875, 0.509375, 0.44375, 0.584375, 0.565625, 0.78125,
              0.53125, 0.571875, 0.5546875, 0.4515625, 0.246875, 0.4515625,
              0.6671875,
            ],
            avg: 0.5762664473684211,
          },
          Georgia: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2421875, 0.33125, 0.4125, 0.64375,
              0.6109375, 0.81875, 0.7109375, 0.215625, 0.375, 0.375, 0.4734375,
              0.64375, 0.2703125, 0.375, 0.2703125, 0.46875, 0.6140625,
              0.4296875, 0.559375, 0.553125, 0.565625, 0.5296875, 0.5671875,
              0.503125, 0.596875, 0.5671875, 0.3125, 0.3125, 0.64375, 0.64375,
              0.64375, 0.4796875, 0.9296875, 0.715625, 0.6546875, 0.6421875,
              0.75, 0.6546875, 0.6, 0.7265625, 0.815625, 0.390625, 0.51875,
              0.7203125, 0.6046875, 0.928125, 0.7671875, 0.7453125, 0.6109375,
              0.7453125, 0.7234375, 0.5625, 0.61875, 0.7578125, 0.70625,
              0.99375, 0.7125, 0.6640625, 0.6015625, 0.375, 0.46875, 0.375,
              0.64375, 0.65, 0.5, 0.5046875, 0.56875, 0.4546875, 0.575,
              0.484375, 0.39375, 0.509375, 0.5828125, 0.29375, 0.3671875,
              0.546875, 0.2875, 0.88125, 0.5921875, 0.5390625, 0.571875,
              0.5640625, 0.4109375, 0.4328125, 0.3453125, 0.5765625, 0.5203125,
              0.75625, 0.50625, 0.5171875, 0.4453125, 0.43125, 0.375, 0.43125,
              0.64375,
            ],
            avg: 0.5551809210526316,
          },
          "Gill Sans": {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2765625, 0.271875, 0.3546875,
              0.584375, 0.5421875, 0.6765625, 0.625, 0.1890625, 0.3234375,
              0.3234375, 0.4171875, 0.584375, 0.2203125, 0.3234375, 0.2203125,
              0.28125, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
              0.2203125, 0.2296875, 0.584375, 0.584375, 0.584375, 0.334375,
              1.0109375, 0.6671875, 0.5640625, 0.709375, 0.75, 0.5, 0.4703125,
              0.740625, 0.7296875, 0.25, 0.3125, 0.65625, 0.490625, 0.78125,
              0.78125, 0.8234375, 0.5109375, 0.8234375, 0.6046875, 0.459375,
              0.6046875, 0.709375, 0.6046875, 1.0421875, 0.709375, 0.6046875,
              0.646875, 0.334375, 0.28125, 0.334375, 0.4703125, 0.5828125,
              0.334375, 0.428125, 0.5, 0.4390625, 0.5109375, 0.4796875,
              0.296875, 0.428125, 0.5, 0.2203125, 0.2265625, 0.5, 0.2203125,
              0.771875, 0.5, 0.553125, 0.5, 0.5, 0.3984375, 0.3859375, 0.334375,
              0.5, 0.4390625, 0.7203125, 0.5, 0.4390625, 0.4171875, 0.334375,
              0.2609375, 0.334375, 0.584375,
            ],
            avg: 0.4933717105263159,
          },
          Helvetica: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2796875, 0.2765625, 0.3546875,
              0.5546875, 0.5546875, 0.8890625, 0.665625, 0.190625, 0.3328125,
              0.3328125, 0.3890625, 0.5828125, 0.2765625, 0.3328125, 0.2765625,
              0.3015625, 0.5546875, 0.5546875, 0.5546875, 0.5546875, 0.5546875,
              0.5546875, 0.5546875, 0.5546875, 0.5546875, 0.5546875, 0.2765625,
              0.2765625, 0.584375, 0.5828125, 0.584375, 0.5546875, 1.0140625,
              0.665625, 0.665625, 0.721875, 0.721875, 0.665625, 0.609375,
              0.7765625, 0.721875, 0.2765625, 0.5, 0.665625, 0.5546875,
              0.8328125, 0.721875, 0.7765625, 0.665625, 0.7765625, 0.721875,
              0.665625, 0.609375, 0.721875, 0.665625, 0.94375, 0.665625,
              0.665625, 0.609375, 0.2765625, 0.3546875, 0.2765625, 0.4765625,
              0.5546875, 0.3328125, 0.5546875, 0.5546875, 0.5, 0.5546875,
              0.5546875, 0.2765625, 0.5546875, 0.5546875, 0.221875, 0.240625,
              0.5, 0.221875, 0.8328125, 0.5546875, 0.5546875, 0.5546875,
              0.5546875, 0.3328125, 0.5, 0.2765625, 0.5546875, 0.5, 0.721875,
              0.5, 0.5, 0.5, 0.3546875, 0.259375, 0.353125, 0.5890625,
            ],
            avg: 0.5279276315789471,
          },
          "Helvetica Neue": {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.278125, 0.259375, 0.4265625,
              0.55625, 0.55625, 1, 0.6453125, 0.278125, 0.2703125, 0.26875,
              0.353125, 0.6, 0.278125, 0.3890625, 0.278125, 0.36875, 0.55625,
              0.55625, 0.55625, 0.55625, 0.55625, 0.55625, 0.55625, 0.55625,
              0.55625, 0.55625, 0.278125, 0.278125, 0.6, 0.6, 0.6, 0.55625, 0.8,
              0.6625, 0.6859375, 0.7234375, 0.7046875, 0.6125, 0.575, 0.759375,
              0.7234375, 0.259375, 0.5203125, 0.6703125, 0.55625, 0.871875,
              0.7234375, 0.7609375, 0.6484375, 0.7609375, 0.6859375, 0.6484375,
              0.575, 0.7234375, 0.6140625, 0.9265625, 0.6125, 0.6484375, 0.6125,
              0.259375, 0.36875, 0.259375, 0.6, 0.5, 0.25625, 0.5375, 0.59375,
              0.5375, 0.59375, 0.5375, 0.2984375, 0.575, 0.55625, 0.2234375,
              0.2375, 0.5203125, 0.2234375, 0.853125, 0.55625, 0.575, 0.59375,
              0.59375, 0.334375, 0.5, 0.315625, 0.55625, 0.5, 0.759375, 0.51875,
              0.5, 0.48125, 0.334375, 0.2234375, 0.334375, 0.6,
            ],
            avg: 0.5279440789473684,
          },
          "Hoefler Text": {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2359375, 0.2234375, 0.3921875,
              0.7125, 0.49375, 0.8859375, 0.771875, 0.2125, 0.3078125, 0.309375,
              0.375, 0.4234375, 0.234375, 0.3125, 0.234375, 0.3, 0.5828125,
              0.365625, 0.434375, 0.3921875, 0.5234375, 0.3984375, 0.5125,
              0.4328125, 0.46875, 0.5125, 0.234375, 0.234375, 0.515625,
              0.4234375, 0.515625, 0.340625, 0.7609375, 0.7359375, 0.6359375,
              0.721875, 0.8125, 0.6375, 0.5875, 0.8078125, 0.853125, 0.4296875,
              0.503125, 0.78125, 0.609375, 0.9609375, 0.8515625, 0.8140625,
              0.6125, 0.8140625, 0.71875, 0.49375, 0.7125, 0.76875, 0.771875,
              1.125, 0.7765625, 0.7734375, 0.65625, 0.321875, 0.3078125,
              0.321875, 0.3546875, 0.5, 0.3375, 0.446875, 0.5359375, 0.45,
              0.5296875, 0.4546875, 0.425, 0.4921875, 0.54375, 0.2671875,
              0.240625, 0.5390625, 0.25, 0.815625, 0.5375, 0.5234375, 0.5390625,
              0.5421875, 0.365625, 0.36875, 0.35625, 0.5171875, 0.5015625, 0.75,
              0.5, 0.509375, 0.44375, 0.2421875, 0.14375, 0.2421875, 0.35,
            ],
            avg: 0.5116447368421051,
          },
          Montserrat: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2625, 0.2609375, 0.3734375,
              0.696875, 0.615625, 0.8296875, 0.6703125, 0.203125, 0.3296875,
              0.3296875, 0.3875, 0.575, 0.2125, 0.3828125, 0.2125, 0.3953125,
              0.6625, 0.3625, 0.56875, 0.5640625, 0.6625, 0.5671875, 0.609375,
              0.5890625, 0.6390625, 0.609375, 0.2125, 0.2125, 0.575, 0.575,
              0.575, 0.5671875, 1.034375, 0.7171875, 0.7546875, 0.7203125,
              0.8265625, 0.6703125, 0.634375, 0.7734375, 0.8140625, 0.303125,
              0.5078125, 0.7125, 0.5890625, 0.95625, 0.8140625, 0.8390625,
              0.71875, 0.8390625, 0.7234375, 0.615625, 0.575, 0.7921875,
              0.6984375, 1.1125, 0.65625, 0.6359375, 0.6515625, 0.31875,
              0.396875, 0.31875, 0.5765625, 0.5, 0.6, 0.590625, 0.678125,
              0.5640625, 0.678125, 0.6046875, 0.375, 0.6875, 0.678125,
              0.2703125, 0.365625, 0.6015625, 0.2703125, 1.0625, 0.678125,
              0.628125, 0.678125, 0.678125, 0.4015625, 0.4890625, 0.40625,
              0.6734375, 0.5421875, 0.8796875, 0.534375, 0.5671875, 0.5125,
              0.334375, 0.2953125, 0.334375, 0.575,
            ],
            avg: 0.571792763157895,
          },
          monospace: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5984375, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6078125, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.61875, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.615625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6140625, 0.6015625, 0.6015625, 0.6015625, 0.6015625, 0.6015625,
              0.6015625, 0.6015625,
            ],
            avg: 0.6020559210526316,
          },
          Overpass: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2296875, 0.2765625, 0.4203125,
              0.68125, 0.584375, 0.8515625, 0.7015625, 0.2203125, 0.3453125,
              0.3453125, 0.53125, 0.63125, 0.2234375, 0.3953125, 0.2234375,
              0.509375, 0.65, 0.4046875, 0.6171875, 0.60625, 0.6484375, 0.60625,
              0.6015625, 0.5375, 0.615625, 0.6015625, 0.2234375, 0.2234375,
              0.63125, 0.63125, 0.63125, 0.5015625, 0.8203125, 0.696875,
              0.6671875, 0.65, 0.6859375, 0.6015625, 0.559375, 0.690625,
              0.7078125, 0.2953125, 0.565625, 0.678125, 0.58125, 0.8046875,
              0.7109375, 0.740625, 0.6421875, 0.740625, 0.6765625, 0.6046875,
              0.590625, 0.696875, 0.6640625, 0.853125, 0.65, 0.6671875, 0.6625,
              0.3734375, 0.509375, 0.3734375, 0.63125, 0.5125, 0.4, 0.5328125,
              0.5625, 0.51875, 0.5625, 0.546875, 0.3359375, 0.5625, 0.565625,
              0.25625, 0.3203125, 0.55, 0.265625, 0.85, 0.565625, 0.5671875,
              0.5625, 0.5625, 0.4046875, 0.4765625, 0.3796875, 0.565625,
              0.521875, 0.7265625, 0.53125, 0.5390625, 0.5125, 0.3671875, 0.275,
              0.3671875, 0.63125,
            ],
            avg: 0.5430756578947369,
          },
          Palatino: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0.278125, 0.371875, 0.60625,
              0.5, 0.840625, 0.778125, 0.209375, 0.334375, 0.334375, 0.390625,
              0.60625, 0.2578125, 0.334375, 0.25, 0.60625, 0.5, 0.5, 0.5, 0.5,
              0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.60625, 0.60625,
              0.60625, 0.4453125, 0.7484375, 0.778125, 0.6109375, 0.709375,
              0.775, 0.6109375, 0.55625, 0.7640625, 0.8328125, 0.3375, 0.346875,
              0.7265625, 0.6109375, 0.946875, 0.83125, 0.7875, 0.6046875,
              0.7875, 0.66875, 0.525, 0.6140625, 0.778125, 0.7234375, 1,
              0.6671875, 0.6671875, 0.6671875, 0.334375, 0.60625, 0.334375,
              0.60625, 0.5, 0.334375, 0.5, 0.565625, 0.4453125, 0.6109375,
              0.4796875, 0.340625, 0.55625, 0.5828125, 0.2921875, 0.2671875,
              0.5640625, 0.2921875, 0.8828125, 0.5828125, 0.546875, 0.6015625,
              0.5609375, 0.3953125, 0.425, 0.3265625, 0.603125, 0.565625,
              0.834375, 0.5171875, 0.55625, 0.5, 0.334375, 0.60625, 0.334375,
              0.60625,
            ],
            avg: 0.5408552631578947,
          },
          RedHatText: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2328125, 0.2203125, 0.35625,
              0.6890625, 0.55, 0.7390625, 0.6703125, 0.2140625, 0.4015625,
              0.4015625, 0.4546875, 0.53125, 0.2203125, 0.45625, 0.2203125,
              0.515625, 0.6609375, 0.3078125, 0.5484375, 0.5875, 0.61875,
              0.5703125, 0.6203125, 0.559375, 0.6140625, 0.6203125, 0.2203125,
              0.2234375, 0.465625, 0.534375, 0.465625, 0.5125, 0.7671875,
              0.6609375, 0.6703125, 0.7265625, 0.728125, 0.6203125, 0.6109375,
              0.8, 0.73125, 0.253125, 0.6, 0.6125, 0.6078125, 0.8625, 0.7390625,
              0.8109375, 0.6546875, 0.809375, 0.6484375, 0.6234375, 0.6171875,
              0.7125, 0.6609375, 0.8984375, 0.6546875, 0.646875, 0.60625,
              0.3625, 0.5203125, 0.3625, 0.540625, 0.4609375, 0.5234375,
              0.5265625, 0.584375, 0.509375, 0.5828125, 0.5578125, 0.3703125,
              0.5828125, 0.553125, 0.2234375, 0.24375, 0.4890625, 0.2234375,
              0.8453125, 0.553125, 0.58125, 0.584375, 0.5828125, 0.353125,
              0.453125, 0.378125, 0.553125, 0.5015625, 0.6984375, 0.4875,
              0.4984375, 0.459375, 0.3953125, 0.2921875, 0.3953125, 0.58125,
            ],
            avg: 0.5341940789473685,
          },
          "sans-serif": {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.278125, 0.278125, 0.35625,
              0.55625, 0.55625, 0.890625, 0.6671875, 0.1921875, 0.334375,
              0.334375, 0.390625, 0.584375, 0.278125, 0.334375, 0.278125,
              0.303125, 0.55625, 0.55625, 0.55625, 0.55625, 0.55625, 0.55625,
              0.55625, 0.55625, 0.55625, 0.55625, 0.278125, 0.278125, 0.5859375,
              0.584375, 0.5859375, 0.55625, 1.015625, 0.6671875, 0.6671875,
              0.7234375, 0.7234375, 0.6671875, 0.6109375, 0.778125, 0.7234375,
              0.278125, 0.5, 0.6671875, 0.55625, 0.834375, 0.7234375, 0.778125,
              0.6671875, 0.778125, 0.7234375, 0.6671875, 0.6109375, 0.7234375,
              0.6671875, 0.9453125, 0.6671875, 0.6671875, 0.6109375, 0.278125,
              0.35625, 0.278125, 0.478125, 0.55625, 0.334375, 0.55625, 0.55625,
              0.5, 0.55625, 0.55625, 0.278125, 0.55625, 0.55625, 0.2234375,
              0.2421875, 0.5, 0.2234375, 0.834375, 0.55625, 0.55625, 0.55625,
              0.55625, 0.334375, 0.5, 0.278125, 0.55625, 0.5, 0.7234375, 0.5,
              0.5, 0.5, 0.35625, 0.2609375, 0.3546875, 0.590625,
            ],
            avg: 0.5293256578947368,
          },
          Seravek: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.215625, 0.296875, 0.4171875,
              0.6734375, 0.4953125, 0.9125, 0.740625, 0.2421875, 0.3375, 0.3375,
              0.409375, 0.60625, 0.2609375, 0.35625, 0.25625, 0.41875,
              0.5921875, 0.3515625, 0.475, 0.4875, 0.5375, 0.509375, 0.5484375,
              0.4546875, 0.5421875, 0.5484375, 0.25625, 0.2546875, 0.5875,
              0.6171875, 0.5875, 0.4578125, 0.8140625, 0.6765625, 0.5703125,
              0.6109375, 0.684375, 0.5109375, 0.4953125, 0.678125, 0.6859375,
              0.2625, 0.2625, 0.5859375, 0.4734375, 0.846875, 0.709375,
              0.740625, 0.509375, 0.740625, 0.584375, 0.5015625, 0.528125,
              0.675, 0.5953125, 0.9453125, 0.596875, 0.540625, 0.540625,
              0.359375, 0.4203125, 0.359375, 0.5109375, 0.421875, 0.4046875,
              0.5015625, 0.5421875, 0.446875, 0.5453125, 0.484375, 0.38125,
              0.5140625, 0.5546875, 0.240625, 0.2640625, 0.490625, 0.2765625,
              0.8625, 0.5546875, 0.546875, 0.5453125, 0.5453125, 0.3625,
              0.41875, 0.3890625, 0.5453125, 0.4703125, 0.7546875, 0.4921875,
              0.4609375, 0.453125, 0.4015625, 0.2640625, 0.4015625, 0.58125,
            ],
            avg: 0.5044078947368421,
          },
          serif: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2484375, 0.334375, 0.409375, 0.5,
              0.5, 0.834375, 0.778125, 0.18125, 0.334375, 0.334375, 0.5,
              0.5640625, 0.25, 0.334375, 0.25, 0.278125, 0.5, 0.5, 0.5, 0.5,
              0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.278125, 0.278125, 0.5640625,
              0.5640625, 0.5640625, 0.4453125, 0.921875, 0.7234375, 0.6671875,
              0.6671875, 0.7234375, 0.6109375, 0.55625, 0.7234375, 0.7234375,
              0.334375, 0.390625, 0.7234375, 0.6109375, 0.890625, 0.7234375,
              0.7234375, 0.55625, 0.7234375, 0.6671875, 0.55625, 0.6109375,
              0.7234375, 0.7234375, 0.9453125, 0.7234375, 0.7234375, 0.6109375,
              0.334375, 0.340625, 0.334375, 0.4703125, 0.5, 0.3453125,
              0.4453125, 0.5, 0.4453125, 0.5, 0.4453125, 0.3828125, 0.5, 0.5,
              0.278125, 0.3359375, 0.5, 0.278125, 0.778125, 0.5, 0.5, 0.5, 0.5,
              0.3375, 0.390625, 0.2796875, 0.5, 0.5, 0.7234375, 0.5, 0.5,
              0.4453125, 0.48125, 0.2015625, 0.48125, 0.5421875,
            ],
            avg: 0.5126315789473684,
          },
          Tahoma: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.3109375, 0.3328125, 0.4015625,
              0.728125, 0.546875, 0.9765625, 0.70625, 0.2109375, 0.3828125,
              0.3828125, 0.546875, 0.728125, 0.303125, 0.3640625, 0.303125,
              0.3953125, 0.546875, 0.546875, 0.546875, 0.546875, 0.546875,
              0.546875, 0.546875, 0.546875, 0.546875, 0.546875, 0.3546875,
              0.3546875, 0.728125, 0.728125, 0.728125, 0.475, 0.909375,
              0.6109375, 0.590625, 0.6015625, 0.6796875, 0.5625, 0.521875,
              0.66875, 0.6765625, 0.3734375, 0.4171875, 0.6046875, 0.4984375,
              0.771875, 0.66875, 0.7078125, 0.5515625, 0.7078125, 0.6375,
              0.5578125, 0.5875, 0.65625, 0.60625, 0.903125, 0.58125, 0.5890625,
              0.559375, 0.3828125, 0.39375, 0.3828125, 0.728125, 0.5625,
              0.546875, 0.525, 0.553125, 0.4625, 0.553125, 0.5265625, 0.3546875,
              0.553125, 0.5578125, 0.2296875, 0.328125, 0.51875, 0.2296875,
              0.840625, 0.5578125, 0.54375, 0.553125, 0.553125, 0.3609375,
              0.446875, 0.3359375, 0.5578125, 0.4984375, 0.7421875, 0.4953125,
              0.4984375, 0.4453125, 0.48125, 0.3828125, 0.48125, 0.728125,
            ],
            avg: 0.5384374999999998,
          },
          "Times New Roman": {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2484375, 0.334375, 0.409375, 0.5,
              0.5, 0.834375, 0.778125, 0.18125, 0.334375, 0.334375, 0.5,
              0.5640625, 0.25, 0.334375, 0.25, 0.28125, 0.5, 0.5, 0.5, 0.5, 0.5,
              0.5, 0.5, 0.5, 0.5, 0.5, 0.278125, 0.278125, 0.5640625, 0.5640625,
              0.5640625, 0.4453125, 0.921875, 0.7234375, 0.6671875, 0.6671875,
              0.7234375, 0.6109375, 0.55625, 0.7234375, 0.7234375, 0.334375,
              0.390625, 0.73125, 0.6109375, 0.890625, 0.7375, 0.7234375,
              0.55625, 0.7234375, 0.6765625, 0.55625, 0.6109375, 0.7234375,
              0.7234375, 0.9453125, 0.7234375, 0.7234375, 0.6109375, 0.334375,
              0.28125, 0.334375, 0.4703125, 0.51875, 0.334375, 0.4453125,
              0.503125, 0.4453125, 0.503125, 0.4453125, 0.4359375, 0.5, 0.5,
              0.278125, 0.35625, 0.50625, 0.278125, 0.778125, 0.5, 0.5,
              0.5046875, 0.5, 0.340625, 0.390625, 0.2796875, 0.5, 0.5,
              0.7234375, 0.5, 0.5, 0.4453125, 0.48125, 0.2015625, 0.48125,
              0.5421875,
            ],
            avg: 0.5134375,
          },
          "Trebuchet MS": {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.3015625, 0.3671875, 0.325,
              0.53125, 0.525, 0.6015625, 0.70625, 0.1609375, 0.3671875,
              0.3671875, 0.3671875, 0.525, 0.3671875, 0.3671875, 0.3671875,
              0.525, 0.525, 0.525, 0.525, 0.525, 0.525, 0.525, 0.525, 0.525,
              0.525, 0.525, 0.3671875, 0.3671875, 0.525, 0.525, 0.525,
              0.3671875, 0.771875, 0.590625, 0.5671875, 0.5984375, 0.6140625,
              0.5359375, 0.525, 0.6765625, 0.6546875, 0.2796875, 0.4765625,
              0.5765625, 0.5078125, 0.7109375, 0.6390625, 0.675, 0.5578125,
              0.7421875, 0.5828125, 0.48125, 0.58125, 0.6484375, 0.5875,
              0.853125, 0.5578125, 0.5703125, 0.5515625, 0.3671875, 0.3578125,
              0.3671875, 0.525, 0.53125, 0.525, 0.5265625, 0.5578125, 0.4953125,
              0.5578125, 0.546875, 0.375, 0.503125, 0.546875, 0.2859375,
              0.3671875, 0.5046875, 0.2953125, 0.83125, 0.546875, 0.5375,
              0.5578125, 0.5578125, 0.3890625, 0.40625, 0.396875, 0.546875,
              0.490625, 0.7453125, 0.5015625, 0.49375, 0.475, 0.3671875, 0.525,
              0.3671875, 0.525,
            ],
            avg: 0.5085197368421052,
          },
          Verdana: {
            widths: [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.35, 0.39375, 0.459375, 0.81875,
              0.6359375, 1.0765625, 0.759375, 0.26875, 0.4546875, 0.4546875,
              0.6359375, 0.81875, 0.3640625, 0.4546875, 0.3640625, 0.4703125,
              0.6359375, 0.6359375, 0.6359375, 0.6359375, 0.6359375, 0.6359375,
              0.6359375, 0.6359375, 0.6359375, 0.6359375, 0.4546875, 0.4546875,
              0.81875, 0.81875, 0.81875, 0.546875, 1, 0.684375, 0.6859375,
              0.6984375, 0.771875, 0.6328125, 0.575, 0.7765625, 0.7515625,
              0.421875, 0.4546875, 0.69375, 0.5578125, 0.84375, 0.7484375,
              0.7875, 0.603125, 0.7875, 0.7, 0.684375, 0.6171875, 0.7328125,
              0.684375, 0.9890625, 0.6859375, 0.615625, 0.6859375, 0.4546875,
              0.46875, 0.4546875, 0.81875, 0.6421875, 0.6359375, 0.6015625,
              0.6234375, 0.521875, 0.6234375, 0.596875, 0.384375, 0.6234375,
              0.6328125, 0.275, 0.3765625, 0.5921875, 0.275, 0.9734375,
              0.6328125, 0.6078125, 0.6234375, 0.6234375, 0.43125, 0.521875,
              0.3953125, 0.6328125, 0.5921875, 0.81875, 0.5921875, 0.5921875,
              0.5265625, 0.6359375, 0.4546875, 0.6359375, 0.81875,
            ],
            avg: 0.6171875000000003,
          },
        },
        h = { mm: 3.8, sm: 38, pt: 1.33, pc: 16, in: 96, px: 1 },
        v = { em: 1, ex: 0.5 },
        y = 1.05,
        m = 1.15,
        g = {
          lineHeight: 1,
          letterSpacing: "0px",
          fontSize: 0,
          angle: 0,
          fontFamily: "",
        },
        b = function (t) {
          return Array.isArray(t) ? t : t.toString().split(/\r\n|\r|\n/g);
        },
        x = function (t, e, n) {
          var r = (function (t) {
            return (t * Math.PI) / 180;
          })(n);
          return Math.abs(Math.cos(r) * t) + Math.abs(Math.sin(r) * e);
        },
        O = function (t, e) {
          var n,
            r =
              null === (n = t.match(/[a-zA-Z%]+/)) || void 0 === n
                ? void 0
                : n[0],
            o = Number(t.match(/[0-9.,]+/));
          return r
            ? h.hasOwnProperty(r)
              ? o * h[r]
              : v.hasOwnProperty(r)
                ? (e ? o * e : o * g.fontSize) * v[r]
                : o
            : o || 0;
        },
        w = function (t, e) {
          var n = Array.isArray(t) ? t[e] : t,
            r = i()({}, n, g);
          return l()({}, r, {
            fontFamily: r.fontFamily,
            letterSpacing:
              "number" === typeof r.letterSpacing
                ? r.letterSpacing
                : O(String(r.letterSpacing), r.fontSize),
            fontSize:
              "number" === typeof r.fontSize
                ? r.fontSize
                : O(String(r.fontSize)),
          });
        },
        C = function (t, e) {
          if (void 0 === t || "" === t || null === t) return 0;
          var n = b(t).map(function (t, n) {
            var r = t.toString().length,
              o = w(e, n),
              a = o.fontSize,
              i = o.letterSpacing,
              c = (function (t) {
                var e =
                  t
                    .split(",")
                    .map(function (t) {
                      return t.replace(/'|"/g, "");
                    })
                    .find(function (t) {
                      return d[t];
                    }) || "Helvetica";
                return d[e];
              })(o.fontFamily);
            return (
              t
                .toString()
                .split("")
                .map(function (t) {
                  return t.charCodeAt(0) < c.widths.length
                    ? c.widths[t.charCodeAt(0)]
                    : c.avg;
                })
                .reduce(function (t, e) {
                  return e + t;
                }, 0) *
                a +
              i * Math.max(r - 1, 0)
            );
          });
          return Math.max.apply(Math, s(n));
        },
        S = function (t, e) {
          var n = Array.isArray(e) ? e[0] && e[0].angle : e && e.angle,
            r = (function (t, e) {
              return void 0 === t || "" === t || null === t
                ? 0
                : b(t).reduce(function (t, n, r) {
                    var o = w(e, r),
                      a = n.toString().match(/[(A-Z)(0-9)]/)
                        ? o.fontSize * m
                        : o.fontSize;
                    return t + o.lineHeight * a;
                  }, 0);
            })(t, e),
            o = C(t, e);
          return {
            width: n ? x(o, r, n) : o,
            height: (n ? x(r, o, n) : r) * y,
          };
        },
        A = o()(function () {
          var t = document.createElementNS("http://www.w3.org/2000/svg", "svg");
          t.setAttribute("xlink", "http://www.w3.org/1999/xlink"),
            t.setAttribute("width", "300"),
            t.setAttribute("height", "300"),
            t.setAttribute("viewBox", "0 0 300 300"),
            t.setAttribute("aria-hidden", "true");
          var e = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "text",
          );
          return (
            t.appendChild(e),
            (t.style.position = "fixed"),
            (t.style.top = "-9999px"),
            (t.style.left = "-9999px"),
            document.body.appendChild(t),
            e
          );
        }),
        j = function (t) {
          return t
            ? ""
                .concat(t.angle, ":")
                .concat(t.fontFamily, ":")
                .concat(t.fontSize, ":")
                .concat(t.letterSpacing, ":")
                .concat(t.lineHeight)
            : "null";
        },
        k = o()(
          function (t, e) {
            var n = A(),
              r = b(t),
              o = 0;
            for (var a of r.entries()) {
              var i = u(a, 2),
                c = i[0],
                l = i[1],
                s = document.createElementNS(
                  "http://www.w3.org/2000/svg",
                  "tspan",
                ),
                f = w(e, c);
              (s.style.fontFamily = f.fontFamily),
                (s.style.fontSize = "".concat(f.fontSize, "px")),
                (s.style.lineHeight = f.lineHeight),
                (s.style.fontFamily = f.fontFamily),
                (s.style.letterSpacing = f.letterSpacing),
                (s.textContent = l),
                s.setAttribute("x", "0"),
                s.setAttribute("y", "".concat(o)),
                n.appendChild(s),
                (o += f.lineHeight * s.getBoundingClientRect().height);
            }
            var p = n.getBoundingClientRect().width;
            return (
              (n.innerHTML = ""),
              {
                width:
                  null !== e && void 0 !== e && e.angle
                    ? x(p, o, null === e || void 0 === e ? void 0 : e.angle)
                    : p,
                height:
                  null !== e && void 0 !== e && e.angle
                    ? x(o, p, null === e || void 0 === e ? void 0 : e.angle)
                    : o,
              }
            );
          },
          function (t, e) {
            var n = Array.isArray(t) ? t.join() : t,
              r = Array.isArray(e) ? e.map(j).join() : j(e);
            return "".concat(n, "::").concat(r);
          },
        ),
        P = function (t, e) {
          var n =
            arguments.length > 2 && void 0 !== arguments[2] && arguments[2];
          return !(
            "undefined" !== typeof window &&
            "undefined" !== typeof window.document &&
            "undefined" !== typeof window.document.createElement
          ) || n
            ? S(t, e)
            : k(t, e);
        },
        E = function (t, e) {
          return P(t, e);
        };
    },
    91002: (t, e, n) => {
      "use strict";
      n.d(e, { Z: () => A });
      var r,
        o,
        a = n(72791),
        i = 0,
        c = 0,
        l = 0,
        u = 1e3,
        s = 0,
        f = 0,
        p = 0,
        d =
          "object" === typeof performance && performance.now
            ? performance
            : Date,
        h =
          "object" === typeof window && window.requestAnimationFrame
            ? window.requestAnimationFrame.bind(window)
            : function (t) {
                setTimeout(t, 17);
              };
      function v() {
        return f || (h(y), (f = d.now() + p));
      }
      function y() {
        f = 0;
      }
      function m() {
        this._call = this._time = this._next = null;
      }
      function g(t, e, n) {
        var r = new m();
        return r.restart(t, e, n), r;
      }
      function b() {
        (f = (s = d.now()) + p), (i = c = 0);
        try {
          !(function () {
            v(), ++i;
            for (var t, e = r; e; )
              (t = f - e._time) >= 0 && e._call.call(void 0, t), (e = e._next);
            --i;
          })();
        } finally {
          (i = 0),
            (function () {
              var t,
                e,
                n = r,
                a = 1 / 0;
              for (; n; )
                n._call
                  ? (a > n._time && (a = n._time), (t = n), (n = n._next))
                  : ((e = n._next),
                    (n._next = null),
                    (n = t ? (t._next = e) : (r = e)));
              (o = t), O(a);
            })(),
            (f = 0);
        }
      }
      function x() {
        var t = d.now(),
          e = t - s;
        e > u && ((p -= e), (s = t));
      }
      function O(t) {
        i ||
          (c && (c = clearTimeout(c)),
          t - f > 24
            ? (t < 1 / 0 && (c = setTimeout(b, t - d.now() - p)),
              l && (l = clearInterval(l)))
            : (l || ((s = d.now()), (l = setInterval(x, u))), (i = 1), h(b)));
      }
      function w(t, e) {
        for (var n = 0; n < e.length; n++) {
          var r = e[n];
          (r.enumerable = r.enumerable || !1),
            (r.configurable = !0),
            "value" in r && (r.writable = !0),
            Object.defineProperty(t, r.key, r);
        }
      }
      m.prototype = g.prototype = {
        constructor: m,
        restart: function (t, e, n) {
          if ("function" !== typeof t)
            throw new TypeError("callback is not a function");
          (n = (null == n ? v() : +n) + (null == e ? 0 : +e)),
            this._next ||
              o === this ||
              (o ? (o._next = this) : (r = this), (o = this)),
            (this._call = t),
            (this._time = n),
            O();
        },
        stop: function () {
          this._call && ((this._call = null), (this._time = 1 / 0), O());
        },
      };
      var C = (function () {
          function t() {
            var e = this;
            !(function (t, e) {
              if (!(t instanceof e))
                throw new TypeError("Cannot call a class as a function");
            })(this, t),
              (this.shouldAnimate = void 0),
              (this.subscribers = void 0),
              (this.activeSubscriptions = void 0),
              (this.timer = void 0),
              (this.loop = function () {
                e.subscribers.forEach(function (t) {
                  t.callback(v() - t.startTime, t.duration);
                });
              }),
              (this.shouldAnimate = !0),
              (this.subscribers = []),
              (this.timer = null),
              (this.activeSubscriptions = 0);
          }
          var e, n, r;
          return (
            (e = t),
            (n = [
              {
                key: "bypassAnimation",
                value: function () {
                  this.shouldAnimate = !1;
                },
              },
              {
                key: "resumeAnimation",
                value: function () {
                  this.shouldAnimate = !0;
                },
              },
              {
                key: "start",
                value: function () {
                  this.timer || (this.timer = g(this.loop));
                },
              },
              {
                key: "stop",
                value: function () {
                  this.timer && (this.timer.stop(), (this.timer = null));
                },
              },
              {
                key: "subscribe",
                value: function (t, e) {
                  e = this.shouldAnimate ? e : 0;
                  var n = this.subscribers.push({
                    startTime: v(),
                    callback: t,
                    duration: e,
                  });
                  return this.activeSubscriptions++, this.start(), n;
                },
              },
              {
                key: "unsubscribe",
                value: function (t) {
                  null !== t &&
                    this.subscribers[t - 1] &&
                    (delete this.subscribers[t - 1],
                    this.activeSubscriptions--),
                    0 === this.activeSubscriptions && this.stop();
                },
              },
            ]) && w(e.prototype, n),
            r && w(e, r),
            Object.defineProperty(e, "prototype", { writable: !1 }),
            t
          );
        })(),
        S = a.createContext({
          transitionTimer: new C(),
          animationTimer: new C(),
        });
      S.displayName = "TimerContext";
      const A = S;
    },
    5129: (t, e, n) => {
      "use strict";
      n.d(e, { A: () => y, C: () => m });
      var r = n(12742),
        o = n.n(r),
        a = n(2100),
        i = n.n(a),
        c = n(66933),
        l = n.n(c),
        u = n(15687),
        s = n.n(u),
        f = n(72791);
      function p(t, e) {
        return (t.key || e).toString();
      }
      function d(t) {
        return t.reduce(function (t, e, n) {
          return (t[p(e, n)] = e), t;
        }, {});
      }
      function h(t, e) {
        var n = !1,
          r = o()(t).reduce(function (t, r) {
            return r in e || ((n = !0), (t[r] = !0)), t;
          }, {});
        return n && r;
      }
      function v(t) {
        return t.type && t.type.getData
          ? t.type.getData(t.props)
          : (t.props && t.props.data) || !1;
      }
      function y(t, e) {
        var n = !1,
          r = !1,
          o = function (t, e) {
            if (!e || t.type !== e.type) return {};
            var o =
                (function (t, e) {
                  var n = t && d(t),
                    r = e && d(e);
                  return { entering: n && h(r, n), exiting: r && h(n, r) };
                })(v(t), v(e)) || {},
              a = o.entering,
              i = o.exiting;
            return (
              (n = n || !!i),
              (r = r || !!a),
              { entering: a || !1, exiting: i || !1 }
            );
          },
          a = function (t, e) {
            return t.map(function (n, r) {
              return n && n.props && n.props.children && e[r]
                ? a(
                    f.Children.toArray(t[r].props.children),
                    f.Children.toArray(e[r].props.children),
                  )
                : o(n, e[r]);
            });
          },
          i = a(f.Children.toArray(t), f.Children.toArray(e));
        return {
          nodesWillExit: n,
          nodesWillEnter: r,
          childrenTransitions: i,
          nodesShouldEnter: !1,
        };
      }
      function m(t, e, n) {
        var r = e && e.nodesWillExit,
          o = e && e.nodesWillEnter,
          a = e && e.nodesShouldEnter,
          c = e && e.nodesShouldLoad,
          u = e && e.nodesDoneLoad,
          f = (e && e.childrenTransitions) || [],
          d = {
            enter: t.animate && t.animate.onEnter && t.animate.onEnter.duration,
            exit: t.animate && t.animate.onExit && t.animate.onExit.duration,
            load: t.animate && t.animate.onLoad && t.animate.onLoad.duration,
            move: t.animate && t.animate.duration,
          },
          h = function (t, e, r) {
            return c
              ? (function (t, e, n) {
                  if (
                    (t = s()({}, t, { onEnd: n })) &&
                    t.onLoad &&
                    !t.onLoad.duration
                  )
                    return { animate: t, data: e };
                  var r = t.onLoad && t.onLoad.after ? t.onLoad.after : i();
                  return {
                    animate: t,
                    data: (e = e.map(function (t, n) {
                      return s()({}, t, r(t, n, e));
                    })),
                  };
                })(r, e, function () {
                  n({ nodesShouldLoad: !1, nodesDoneLoad: !0 });
                })
              : (function (t, e, n, r) {
                  if (
                    (t = s()({}, t, { onEnd: r })) &&
                    t.onLoad &&
                    !t.onLoad.duration
                  )
                    return { animate: t, data: n };
                  var o = t.onLoad && t.onLoad.before ? t.onLoad.before : i();
                  return {
                    animate: t,
                    data: (n = n.map(function (t, e) {
                      return s()({}, t, o(t, e, n));
                    })),
                    clipWidth: 0,
                  };
                })(r, 0, e, function () {
                  n({ nodesDoneLoad: !0 });
                });
          },
          y = function (t, e, r, o) {
            return (function (t, e, n, r, o) {
              var a = t && t.onExit;
              if (((t = s()({}, t, a)), r)) {
                t.onEnd = o;
                var c = t.onExit && t.onExit.before ? t.onExit.before : i();
                n = n.map(function (t, e) {
                  var o = (t.key || e).toString();
                  return r[o] ? s()({}, t, c(t, e, n)) : t;
                });
              }
              return { animate: t, data: n };
            })(o, 0, r, t, function () {
              n({ nodesWillExit: !1 });
            });
          },
          m = function (t, e, r, o) {
            return a
              ? (function (t, e, n, r) {
                  var o = t && t.onEnter;
                  if (((t = s()({}, t, o)), n)) {
                    t.onEnd = r;
                    var a =
                      t.onEnter && t.onEnter.after ? t.onEnter.after : i();
                    e = e.map(function (t, r) {
                      var o = p(t, r);
                      return n[o] ? s()({}, t, a(t, r, e)) : t;
                    });
                  }
                  return { animate: t, data: e };
                })(o, r, t, function () {
                  n({ nodesWillEnter: !1 });
                })
              : (function (t, e, n, r, o) {
                  if (r) {
                    var a =
                      (t = s()({}, t, { onEnd: o })).onEnter && t.onEnter.before
                        ? t.onEnter.before
                        : i();
                    n = n.map(function (t, e) {
                      var o = (t.key || e).toString();
                      return r[o] ? s()({}, t, a(t, e, n)) : t;
                    });
                  }
                  return { animate: t, data: n };
                })(o, 0, r, t, function () {
                  n({ nodesShouldEnter: !0 });
                });
          },
          g = function (t, e) {
            var n = t.props.animate;
            if (!t.type) return {};
            var r =
              (t.props && t.props.polar && t.type.defaultPolarTransitions) ||
              t.type.defaultTransitions;
            if (r) {
              var o = n[e] && n[e].duration;
              return void 0 !== o ? o : r[e] && r[e].duration;
            }
            return {};
          };
        return function (n, c) {
          var p = v(n) || [],
            b = l()({}, t.animate, n.props.animate),
            x =
              (n.props.polar && n.type.defaultPolarTransitions) ||
              n.type.defaultTransitions;
          (b.onExit = l()({}, b.onExit, x && x.onExit)),
            (b.onEnter = l()({}, b.onEnter, x && x.onEnter)),
            (b.onLoad = l()({}, b.onLoad, x && x.onLoad));
          var O = f[c] || f[0];
          if (!u) {
            var w = { duration: void 0 !== d.load ? d.load : g(n, "onLoad") };
            return h(0, p, s()({}, b, w));
          }
          if (r) {
            var C = O && O.exiting,
              S = void 0 !== d.exit ? d.exit : g(n, "onExit"),
              A = C ? { duration: S } : { delay: S };
            return y(C, 0, p, s()({}, b, A));
          }
          if (o) {
            var j = O && O.entering,
              k = void 0 !== d.enter ? d.enter : g(n, "onEnter"),
              P =
                void 0 !== d.move
                  ? d.move
                  : n.props.animate && n.props.animate.duration,
              E = { duration: a && j ? k : P };
            return m(j, 0, p, s()({}, b, E));
          }
          return !e && b && b.onExit
            ? (function (t, e) {
                var n = t.onEnter && t.onEnter.after ? t.onEnter.after : i();
                return {
                  data: e.map(function (t, r) {
                    return s()({}, t, n(t, r, e));
                  }),
                };
              })(b, p)
            : { animate: b, data: p };
        };
      }
    },
    97409: (t, e, n) => {
      "use strict";
      n.d(e, { I: () => f, h: () => p });
      var r = n(72791);
      function o(t, e) {
        return (
          (function (t) {
            if (Array.isArray(t)) return t;
          })(t) ||
          (function (t, e) {
            var n =
              null == t
                ? null
                : ("undefined" !== typeof Symbol && t[Symbol.iterator]) ||
                  t["@@iterator"];
            if (null == n) return;
            var r,
              o,
              a = [],
              i = !0,
              c = !1;
            try {
              for (
                n = n.call(t);
                !(i = (r = n.next()).done) &&
                (a.push(r.value), !e || a.length !== e);
                i = !0
              );
            } catch (l) {
              (c = !0), (o = l);
            } finally {
              try {
                i || null == n.return || n.return();
              } finally {
                if (c) throw o;
              }
            }
            return a;
          })(t, e) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return a(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return a(t, e);
          })(t, e) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function a(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function i(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function c(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      var l = { startsWith: ["data-", "aria-"], exactMatch: [] },
        u = function (t) {
          return !(
            !(function (t) {
              var e = !1;
              return (
                l.startsWith.forEach(function (n) {
                  new RegExp("\\b(".concat(n, ")(\\w|-)+"), "g").test(t) &&
                    (e = !0);
                }),
                e
              );
            })(t) &&
            !(function (t) {
              return l.exactMatch.includes(t);
            })(t)
          );
        },
        s = function (t, e) {
          return "function" === typeof t ? t(e) : t;
        },
        f = function (t) {
          var e = (function (t) {
            for (var e = 1; e < arguments.length; e++) {
              var n = null != arguments[e] ? arguments[e] : {};
              e % 2
                ? i(Object(n), !0).forEach(function (e) {
                    c(t, e, n[e]);
                  })
                : Object.getOwnPropertyDescriptors
                  ? Object.defineProperties(
                      t,
                      Object.getOwnPropertyDescriptors(n),
                    )
                  : i(Object(n)).forEach(function (e) {
                      Object.defineProperty(
                        t,
                        e,
                        Object.getOwnPropertyDescriptor(n, e),
                      );
                    });
            }
            return t;
          })({}, t);
          return Object.fromEntries(
            Object.entries(e)
              .filter(function (t) {
                var e = o(t, 1)[0];
                return u(e);
              })
              .map(function (e) {
                var n = o(e, 2),
                  r = n[0],
                  a = n[1];
                return [r, s(a, t)];
              }),
          );
        },
        p = function (t, e) {
          return r.cloneElement(t, f(e));
        };
    },
    71472: (t, e, n) => {
      "use strict";
      n.d(e, {
        C2: () => U,
        CP: () => V,
        D8: () => R,
        IP: () => z,
        Oz: () => H,
        ge: () => W,
        ny: () => B,
        yZ: () => F,
      });
      var r = n(93977),
        o = n.n(r),
        a = n(92063),
        i = n.n(a),
        c = n(66339),
        l = n.n(c),
        u = n(98444),
        s = n.n(u),
        f = n(72064),
        p = n.n(f),
        d = n(74786),
        h = n.n(d),
        v = n(25506),
        y = n.n(v),
        m = n(66933),
        g = n.n(m),
        b = n(15687),
        x = n.n(b),
        O = n(72791),
        w = n(4463),
        C = n(30637),
        S = n(54481),
        A = n(28275),
        j = n(79704),
        k = n(15896),
        P = n(8091),
        E = n(20933),
        M = n(40143);
      function T(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return _(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          (function (t, e) {
            if (!t) return;
            if ("string" === typeof t) return _(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(t);
            if (
              "Arguments" === n ||
              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
            )
              return _(t, e);
          })(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function _(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function L(t, e) {
        var n = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
          var r = Object.getOwnPropertySymbols(t);
          e &&
            (r = r.filter(function (e) {
              return Object.getOwnPropertyDescriptor(t, e).enumerable;
            })),
            n.push.apply(n, r);
        }
        return n;
      }
      function D(t) {
        for (var e = 1; e < arguments.length; e++) {
          var n = null != arguments[e] ? arguments[e] : {};
          e % 2
            ? L(Object(n), !0).forEach(function (e) {
                I(t, e, n[e]);
              })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n))
              : L(Object(n)).forEach(function (e) {
                  Object.defineProperty(
                    t,
                    e,
                    Object.getOwnPropertyDescriptor(n, e),
                  );
                });
        }
        return t;
      }
      function I(t, e, n) {
        return (
          e in t
            ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0,
              })
            : (t[e] = n),
          t
        );
      }
      function R(t, e) {
        var n = {
            polar: t.polar,
            startAngle: t.startAngle,
            endAngle: t.endAngle,
            categories: t.categories,
            minDomain: t.minDomain,
            maxDomain: t.maxDomain,
          },
          r = 0,
          o = e ? e.slice(0) : O.Children.toArray(t.children);
        n = (function (t) {
          var e = t.children,
            n = t.props,
            r = t.childComponents,
            o = t.parentProps,
            a = e.some(function (t) {
              return t.type && "histogram" === t.type.role;
            }),
            i =
              a &&
              e.length &&
              e.every(function (t) {
                return t.type && "histogram" === t.type.role;
              });
          if (
            (a &&
              !i &&
              M.Z(
                "VictoryHistogram only supports being stacked with other VictoryHistogram components. Check to make sure that you are only passing VictoryHistogram components to VictoryStack",
              ),
            !i)
          )
            return o;
          var c = n.bins || r[0].props.bins;
          if (!Array.isArray(c)) {
            var l = e.reduce(function (t, e) {
              var n = P.$0(e.props.x || "x");
              return t.concat(
                e.props.data.map(function (t) {
                  return { x: n(t) };
                }),
              );
            }, []);
            c = (0, e[0].type.getFormattedData)({ data: l, bins: c }).reduce(
              function (t, e, n) {
                var r = e.x0,
                  o = e.x1;
                return 0 === n ? t.concat([r, o]) : t.concat(o);
              },
              [],
            );
          }
          return D(D({}, o), {}, { bins: c });
        })({ children: o, props: t, childComponents: e, parentProps: n });
        var a = o.filter(function (t) {
            return t.type && "stack" === t.type.role;
          }).length,
          c = P.F1(
            o,
            function (t, e, o) {
              var a,
                i = x()({}, t.props, n);
              return S.hi(t)
                ? ((a =
                    t.type && h()(t.type.getData)
                      ? (t = o ? O.cloneElement(t, o.props) : t).type.getData(i)
                      : S.Yu(i)),
                  (r += 1),
                  a.map(function (t, e) {
                    return x()({ _stack: r, _group: e }, t);
                  }))
                : null;
            },
            t,
            [],
            function (t, e) {
              return t.concat(l()(e, "_group"));
            },
          ),
          u = a ? "_group" : "_stack";
        return i()(s()(c, u));
      }
      function N(t, e, n) {
        var r = t.datasets,
          o = t.horizontal ? P.rx(t, "y") : P.rx(t, "x"),
          a = Math.abs(o[1] - o[0]);
        n = void 0 !== n ? n : (Array.isArray(r[0]) && r[0].length) || 1;
        var i = (e = e || r.length) * n;
        return Math.round((0.5 * a) / i);
      }
      function W(t, e, n) {
        n = n || O.Children.toArray(t.children);
        var r,
          o = A.lP(t, e),
          a = (function (t, e, n) {
            if (!t.polar && "x" === e) {
              var r = n.filter(function (t) {
                return t.type && t.type.role && "group" === t.type.role;
              });
              if (!(r.length < 1)) {
                var o = r[0].props,
                  a = o.offset,
                  i = o.children;
                if (a) {
                  var c = Array.isArray(i) && i[0];
                  if (c) {
                    var l = c.props.barWidth,
                      u = (c.props.data && c.props.data.length) || 1;
                    if (c && "stack" === c.type.role) {
                      var s = c.props.children && c.props.children[0];
                      if (!s) return;
                      (l = s.props.barWidth), (u = c.props.children.length);
                    }
                    var f = l || N(t, i.length, u);
                    return {
                      x: (f * i.length) / 2 + (a - f * ((i.length - 1) / 2)),
                    };
                  }
                }
              }
            }
          })(t, e, n);
        if (o) r = o;
        else {
          var i = A.bZ(t, e),
            c = A.lg(t, e),
            l = (t.data || t.y) && S.Yu(t),
            u = l ? A.$B(t, e, l) : [],
            s = (function (t, e, n) {
              var r = n ? n.slice(0) : O.Children.toArray(t.children),
                o = t.data ? S.Yu(t) : void 0,
                a = t.polar,
                i = t.startAngle,
                c = t.endAngle,
                l = t.categories,
                u = t.minDomain,
                s = t.maxDomain,
                f = {
                  horizontal: t.horizontal,
                  polar: a,
                  startAngle: i,
                  endAngle: c,
                  minDomain: u,
                  maxDomain: s,
                  categories: l,
                },
                p = o ? x()(f, { data: o }) : f,
                d = P.F1(
                  r,
                  function (t) {
                    var n = x()({}, t.props, p);
                    return A.h9(t)
                      ? t.type && h()(t.type.getDomain)
                        ? t.props && t.type.getDomain(n, e)
                        : A.ge(n, e)
                      : null;
                  },
                  t,
                );
              return [
                0 === d.length ? 0 : k.ao(d),
                0 === d.length ? 1 : k.MN(d),
              ];
            })(t, e, n),
            f = i || k.ao([].concat(T(u), T(s))),
            p = c || k.MN([].concat(T(u), T(s)));
          r = A.CU(f, p);
        }
        return A.Rm(r, x()({ domainPadding: a }, t), e);
      }
      function F(t, e, n) {
        if (t.data) return E.q8(t, e);
        var r = n ? n.slice(0) : O.Children.toArray(t.children),
          o = p()(
            P.F1(
              r,
              function (n) {
                var r = x()({}, n.props, { horizontal: t.horizontal });
                return E.md(r, e);
              },
              t,
            ),
          );
        return o.length > 1 ? E.w8("linear") : E.w8(o[0]);
      }
      function z(t) {
        var e = j.pA(t, [
            "groupComponent",
            "containerComponent",
            "labelComponent",
          ]),
          n = t.events;
        return (
          Array.isArray(e) &&
            (n = Array.isArray(t.events) ? e.concat.apply(e, T(t.events)) : e),
          n || []
        );
      }
      function U(t, e, n) {
        var r = t && t[n] && t[n].style ? t[n].style : {};
        return P.Wi(e, r);
      }
      function B(t, e, n) {
        var r = n.style,
          o = n.role,
          a = t.props.style || {};
        if (Array.isArray(a)) return a;
        var i = t.type && t.type.role,
          c =
            "stack" === i
              ? void 0
              : (function (t, e, n) {
                  var r = t.style,
                    o = t.colorScale,
                    a = t.color;
                  if (r && r.data && r.data.fill) return r.data.fill;
                  if (
                    ((o =
                      e.props && e.props.colorScale ? e.props.colorScale : o),
                    (a = e.props && e.props.color ? e.props.color : a),
                    o || a)
                  ) {
                    var i = Array.isArray(o) ? o : C.p(o);
                    return a || i[n % i.length];
                  }
                })(n, t, e),
          l = "line" === i ? { fill: "none", stroke: c } : { fill: c },
          u = "stack" === o ? {} : { width: N(n) },
          s = g()({}, a.data, x()({}, u, r.data, l)),
          f = g()({}, a.labels, r.labels);
        return { parent: r.parent, data: s, labels: f };
      }
      function q(t, e, n) {
        var r = o()(t.categories) ? t.categories[e] : t.categories,
          a = w.OO(n, e),
          i = a ? S.RU(a.props, e) : [],
          c =
            r ||
            (function (t, e) {
              return P.F1(t.slice(0), function (t) {
                var n = t.props || {};
                if (!A.h9(t) || !n.categories) return null;
                var r =
                    n.categories && !Array.isArray(n.categories)
                      ? n.categories[e]
                      : n.props.categories,
                  o =
                    r &&
                    r.filter(function (t) {
                      return "string" === typeof t;
                    });
                return o ? k.o2(o) : [];
              });
            })(n, e);
        return p()(y()([].concat(T(c), T(i))));
      }
      function H(t, e) {
        var n = q(t, "x", (e = e || O.Children.toArray(t.children))),
          r = q(t, "y", e),
          o = (function (t) {
            return P.F1(
              t.slice(0),
              function (t) {
                var e = t.props || {};
                return S.hi(t)
                  ? (t.type && h()(t.type.getData)
                      ? t.type.getData(e)
                      : S.Yu(e)
                    ).map(function (t) {
                      return { x: t.xName, y: t.yName };
                    })
                  : null;
              },
              {},
              { x: [], y: [] },
              function (t, e) {
                var n = Array.isArray(e)
                    ? e
                        .map(function (t) {
                          return t.x;
                        })
                        .filter(Boolean)
                    : e.x,
                  r = Array.isArray(e)
                    ? e
                        .map(function (t) {
                          return t.y;
                        })
                        .filter(Boolean)
                    : e.y;
                return {
                  x: void 0 !== n ? t.x.concat(n) : t.x,
                  y: void 0 !== r ? t.y.concat(r) : t.y,
                };
              },
            );
          })(e);
        return {
          x: p()(y()([].concat(T(n), T(o.x)))),
          y: p()(y()([].concat(T(r), T(o.y)))),
        };
      }
      function V(t, e, n) {
        var r =
            t.categories && !Array.isArray(t.categories)
              ? t.categories.x
              : t.categories,
          o =
            t.categories && !Array.isArray(t.categories)
              ? t.categories.y
              : t.categories,
          a = !r || !o ? n || H(t, e) : {},
          i = r || a.x,
          c = o || a.y;
        return { x: i.length > 0 ? i : void 0, y: c.length > 0 ? c : void 0 };
      }
    },
    68973: (t, e, n) => {
      "use strict";
      n.d(e, { Z: () => N });
      var r = n(71180),
        o = n.n(r),
        a = n(12742),
        i = n.n(a),
        c = n(99305),
        l = n.n(c),
        u = n(66364),
        s = n.n(u),
        f = n(66933),
        p = n.n(f),
        d = n(74786),
        h = n.n(d),
        v = n(15687),
        y = n.n(v),
        m = n(72791),
        g = n(52007),
        b = n.n(g),
        x = n(79704),
        O = n(8091),
        w = n(42745),
        C = n(91002),
        S = n(50077),
        A = n.n(S),
        j = n(72451),
        k = n.n(j);
      function P(t, e) {
        return (
          (function (t) {
            if (Array.isArray(t)) return t;
          })(t) ||
          (function (t, e) {
            var n =
              null == t
                ? null
                : ("undefined" !== typeof Symbol && t[Symbol.iterator]) ||
                  t["@@iterator"];
            if (null == n) return;
            var r,
              o,
              a = [],
              i = !0,
              c = !1;
            try {
              for (
                n = n.call(t);
                !(i = (r = n.next()).done) &&
                (a.push(r.value), !e || a.length !== e);
                i = !0
              );
            } catch (l) {
              (c = !0), (o = l);
            } finally {
              try {
                i || null == n.return || n.return();
              } finally {
                if (c) throw o;
              }
            }
            return a;
          })(t, e) ||
          M(t, e) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function E(t) {
        return (
          (function (t) {
            if (Array.isArray(t)) return T(t);
          })(t) ||
          (function (t) {
            if (
              ("undefined" !== typeof Symbol && null != t[Symbol.iterator]) ||
              null != t["@@iterator"]
            )
              return Array.from(t);
          })(t) ||
          M(t) ||
          (function () {
            throw new TypeError(
              "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
          })()
        );
      }
      function M(t, e) {
        if (t) {
          if ("string" === typeof t) return T(t, e);
          var n = Object.prototype.toString.call(t).slice(8, -1);
          return (
            "Object" === n && t.constructor && (n = t.constructor.name),
            "Map" === n || "Set" === n
              ? Array.from(t)
              : "Arguments" === n ||
                  /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
                ? T(t, e)
                : void 0
          );
        }
      }
      function T(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r;
      }
      function _(t, e) {
        for (var n = 0; n < e.length; n++) {
          var r = e[n];
          (r.enumerable = r.enumerable || !1),
            (r.configurable = !0),
            "value" in r && (r.writable = !0),
            Object.defineProperty(t, r.key, r);
        }
      }
      function L(t, e) {
        return (
          (L = Object.setPrototypeOf
            ? Object.setPrototypeOf.bind()
            : function (t, e) {
                return (t.__proto__ = e), t;
              }),
          L(t, e)
        );
      }
      function D(t) {
        var e = (function () {
          if ("undefined" === typeof Reflect || !Reflect.construct) return !1;
          if (Reflect.construct.sham) return !1;
          if ("function" === typeof Proxy) return !0;
          try {
            return (
              Boolean.prototype.valueOf.call(
                Reflect.construct(Boolean, [], function () {}),
              ),
              !0
            );
          } catch (t) {
            return !1;
          }
        })();
        return function () {
          var n,
            r = R(t);
          if (e) {
            var o = R(this).constructor;
            n = Reflect.construct(r, arguments, o);
          } else n = r.apply(this, arguments);
          return (function (t, e) {
            if (e && ("object" === typeof e || "function" === typeof e))
              return e;
            if (void 0 !== e)
              throw new TypeError(
                "Derived constructors may only return object or undefined",
              );
            return I(t);
          })(this, n);
        };
      }
      function I(t) {
        if (void 0 === t)
          throw new ReferenceError(
            "this hasn't been initialised - super() hasn't been called",
          );
        return t;
      }
      function R(t) {
        return (
          (R = Object.setPrototypeOf
            ? Object.getPrototypeOf.bind()
            : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t);
              }),
          R(t)
        );
      }
      var N = (function (t) {
        !(function (t, e) {
          if ("function" !== typeof e && null !== e)
            throw new TypeError(
              "Super expression must either be null or a function",
            );
          (t.prototype = Object.create(e && e.prototype, {
            constructor: { value: t, writable: !0, configurable: !0 },
          })),
            Object.defineProperty(t, "prototype", { writable: !1 }),
            e && L(t, e);
        })(c, t);
        var e,
          n,
          r,
          a = D(c);
        function c(t) {
          var e;
          return (
            (function (t, e) {
              if (!(t instanceof e))
                throw new TypeError("Cannot call a class as a function");
            })(this, c),
            ((e = a.call(this, t)).state = e.state || {}),
            (e.getScopedEvents = x.$V.bind(I(e))),
            (e.getEventState = x.Ki.bind(I(e))),
            (e.baseProps = e.getBaseProps(t)),
            (e.sharedEventsCache = {}),
            (e.globalEvents = {}),
            (e.prevGlobalEventKeys = []),
            (e.boundGlobalEvents = {}),
            e
          );
        }
        return (
          (e = c),
          (n = [
            {
              key: "shouldComponentUpdate",
              value: function (t) {
                if (!A()(this.props, t)) {
                  this.baseProps = this.getBaseProps(t);
                  var e = this.getExternalMutations(t, this.baseProps);
                  this.applyExternalMutations(t, e);
                }
                return !0;
              },
            },
            {
              key: "componentDidMount",
              value: function () {
                var t = this,
                  e = i()(this.globalEvents);
                e.forEach(function (e) {
                  return t.addGlobalListener(e);
                }),
                  (this.prevGlobalEventKeys = e);
              },
            },
            {
              key: "componentDidUpdate",
              value: function () {
                var t = this,
                  e = i()(this.globalEvents);
                o()(this.prevGlobalEventKeys, e).forEach(function (e) {
                  return t.removeGlobalListener(e);
                }),
                  o()(e, this.prevGlobalEventKeys).forEach(function (e) {
                    return t.addGlobalListener(e);
                  }),
                  (this.prevGlobalEventKeys = e);
              },
            },
            {
              key: "componentWillUnmount",
              value: function () {
                var t = this;
                this.prevGlobalEventKeys.forEach(function (e) {
                  return t.removeGlobalListener(e);
                });
              },
            },
            {
              key: "addGlobalListener",
              value: function (t) {
                var e = this,
                  n = function (n) {
                    var r = e.globalEvents[t];
                    return r && r(x.ss(n));
                  };
                (this.boundGlobalEvents[t] = n),
                  window.addEventListener(x.Ih(t), n);
              },
            },
            {
              key: "removeGlobalListener",
              value: function (t) {
                window.removeEventListener(x.Ih(t), this.boundGlobalEvents[t]);
              },
            },
            {
              key: "getAllEvents",
              value: function (t) {
                var e = x.pA(t, ["container", "groupComponent"]);
                return Array.isArray(e)
                  ? Array.isArray(t.events)
                    ? e.concat.apply(e, E(t.events))
                    : e
                  : t.events;
              },
            },
            {
              key: "applyExternalMutations",
              value: function (t, e) {
                if (!s()(e)) {
                  var n = t.externalEventMutations.reduce(function (t, e) {
                      return (t = h()(e.callback) ? t.concat(e.callback) : t);
                    }, []),
                    r = n.length
                      ? function () {
                          n.forEach(function (t) {
                            return t();
                          });
                        }
                      : void 0;
                  this.setState(e, r);
                }
              },
            },
            {
              key: "getExternalMutations",
              value: function (t, e) {
                return s()(t.externalEventMutations)
                  ? void 0
                  : x.gX(t.externalEventMutations, e, this.state, i()(e));
              },
            },
            {
              key: "cacheSharedEvents",
              value: function (t, e, n) {
                this.sharedEventsCache[t] = [e, n];
              },
            },
            {
              key: "getCachedSharedEvents",
              value: function (t, e) {
                var n = P(this.sharedEventsCache[t] || [], 2),
                  r = n[0],
                  o = n[1];
                if (r && A()(e, o)) return r;
              },
            },
            {
              key: "getBaseProps",
              value: function (t) {
                var e = t.container,
                  n = m.Children.toArray(this.props.children),
                  r = this.getBasePropsFromChildren(n),
                  o = e ? e.props : {};
                return y()({}, r, { parent: o });
              },
            },
            {
              key: "getBasePropsFromChildren",
              value: function (t) {
                var e = O.F1(t, function (t, e) {
                  if (t.type && h()(t.type.getBaseProps)) {
                    var n = t.props && t.type.getBaseProps(t.props);
                    return n ? [[e, n]] : null;
                  }
                  return null;
                });
                return l()(e);
              },
            },
            {
              key: "getNewChildren",
              value: function (t, e) {
                var n = this,
                  r = t.events,
                  o = t.eventKey,
                  a = function (t, i) {
                    return t.reduce(function (t, c, l) {
                      if (c.props.children) {
                        var u = m.Children.toArray(c.props.children),
                          s = i.slice(l, l + u.length),
                          f = m.cloneElement(c, c.props, a(u, s));
                        return t.concat(f);
                      }
                      if (
                        "parent" !== i[l] &&
                        c.type &&
                        h()(c.type.getBaseProps)
                      ) {
                        var p = c.props.name || i[l],
                          d =
                            Array.isArray(r) &&
                            r.filter(function (t) {
                              return (
                                "parent" !== t.target &&
                                (Array.isArray(t.childName)
                                  ? t.childName.indexOf(p) > -1
                                  : t.childName === p || "all" === t.childName)
                              );
                            }),
                          v = [p, e, d, k()(n.state[p])],
                          g = n.getCachedSharedEvents(p, v) || {
                            events: d,
                            getEvents: function (t, r) {
                              return n.getScopedEvents(t, r, p, e);
                            },
                            getEventState: function (t, e) {
                              return n.getEventState(t, e, p);
                            },
                          };
                        return (
                          n.cacheSharedEvents(p, g, v),
                          t.concat(
                            m.cloneElement(
                              c,
                              y()(
                                {
                                  key: "events-".concat(p),
                                  sharedEvents: g,
                                  eventKey: o,
                                  name: p,
                                },
                                c.props,
                              ),
                            ),
                          )
                        );
                      }
                      return t.concat(c);
                    }, []);
                  },
                  c = i()(e),
                  l = m.Children.toArray(t.children);
                return a(l, c);
              },
            },
            {
              key: "getContainer",
              value: function (t, e, n) {
                var r = this,
                  o = this.getNewChildren(t, e),
                  a =
                    Array.isArray(n) &&
                    n.filter(function (t) {
                      return "parent" === t.target;
                    }),
                  i =
                    a.length > 0
                      ? {
                          events: a,
                          getEvents: function (t, n) {
                            return r.getScopedEvents(t, n, null, e);
                          },
                          getEventState: this.getEventState,
                        }
                      : null,
                  c = t.container || t.groupComponent,
                  l = c.type && c.type.role,
                  u = c.props || {},
                  s = x.vw.bind(this),
                  f = i && s({ sharedEvents: i }, "parent"),
                  d = p()(
                    {},
                    this.getEventState("parent", "parent"),
                    u,
                    e.parent,
                    { children: o },
                  ),
                  h = p()({}, x.Z8(f, "parent", d), u.events);
                this.globalEvents = x.hy(h);
                var v = x.fM(h);
                return "container" === l
                  ? m.cloneElement(c, y()({}, d, { events: v }))
                  : m.cloneElement(c, v, o);
              },
            },
            {
              key: "render",
              value: function () {
                var t = this.getAllEvents(this.props);
                return t
                  ? this.getContainer(this.props, this.baseProps, t)
                  : m.cloneElement(this.props.container, {
                      children: this.props.children,
                    });
              },
            },
          ]) && _(e.prototype, n),
          r && _(e, r),
          Object.defineProperty(e, "prototype", { writable: !1 }),
          c
        );
      })(m.Component);
      (N.displayName = "VictorySharedEvents"),
        (N.role = "shared-event-wrapper"),
        (N.propTypes = {
          children: b().oneOfType([b().arrayOf(b().node), b().node]),
          container: b().node,
          eventKey: b().oneOfType([
            b().array,
            b().func,
            w.BO([w._L, w.A7]),
            b().string,
          ]),
          events: b().arrayOf(
            b().shape({
              childName: b().oneOfType([b().string, b().array]),
              eventHandlers: b().object,
              eventKey: b().oneOfType([
                b().array,
                b().func,
                w.BO([w._L, w.A7]),
                b().string,
              ]),
              target: b().string,
            }),
          ),
          externalEventMutations: b().arrayOf(
            b().shape({
              callback: b().func,
              childName: b().oneOfType([b().string, b().array]),
              eventKey: b().oneOfType([
                b().array,
                w.BO([w._L, w.A7]),
                b().string,
              ]),
              mutation: b().func,
              target: b().oneOfType([b().string, b().array]),
            }),
          ),
          groupComponent: b().node,
        }),
        (N.defaultProps = { groupComponent: m.createElement("g", null) }),
        (N.contextType = C.Z);
    },
    14837: (t, e, n) => {
      "use strict";
      function r(t, e) {
        return (
          (t = +t),
          (e = +e),
          function (n) {
            return t * (1 - n) + e * n;
          }
        );
      }
      n.d(e, { Z: () => r });
    },
    67536: (t, e, n) => {
      "use strict";
      function r(t, e, n) {
        (t.prototype = e.prototype = n), (n.constructor = t);
      }
      function o(t, e) {
        var n = Object.create(t.prototype);
        for (var r in e) n[r] = e[r];
        return n;
      }
      function a() {}
      n.d(e, { Z: () => Q });
      var i = 0.7,
        c = 1 / i,
        l = "\\s*([+-]?\\d+)\\s*",
        u = "\\s*([+-]?(?:\\d*\\.)?\\d+(?:[eE][+-]?\\d+)?)\\s*",
        s = "\\s*([+-]?(?:\\d*\\.)?\\d+(?:[eE][+-]?\\d+)?)%\\s*",
        f = /^#([0-9a-f]{3,8})$/,
        p = new RegExp(
          "^rgb\\(".concat(l, ",").concat(l, ",").concat(l, "\\)$"),
        ),
        d = new RegExp(
          "^rgb\\(".concat(s, ",").concat(s, ",").concat(s, "\\)$"),
        ),
        h = new RegExp(
          "^rgba\\("
            .concat(l, ",")
            .concat(l, ",")
            .concat(l, ",")
            .concat(u, "\\)$"),
        ),
        v = new RegExp(
          "^rgba\\("
            .concat(s, ",")
            .concat(s, ",")
            .concat(s, ",")
            .concat(u, "\\)$"),
        ),
        y = new RegExp(
          "^hsl\\(".concat(u, ",").concat(s, ",").concat(s, "\\)$"),
        ),
        m = new RegExp(
          "^hsla\\("
            .concat(u, ",")
            .concat(s, ",")
            .concat(s, ",")
            .concat(u, "\\)$"),
        ),
        g = {
          aliceblue: 15792383,
          antiquewhite: 16444375,
          aqua: 65535,
          aquamarine: 8388564,
          azure: 15794175,
          beige: 16119260,
          bisque: 16770244,
          black: 0,
          blanchedalmond: 16772045,
          blue: 255,
          blueviolet: 9055202,
          brown: 10824234,
          burlywood: 14596231,
          cadetblue: 6266528,
          chartreuse: 8388352,
          chocolate: 13789470,
          coral: 16744272,
          cornflowerblue: 6591981,
          cornsilk: 16775388,
          crimson: 14423100,
          cyan: 65535,
          darkblue: 139,
          darkcyan: 35723,
          darkgoldenrod: 12092939,
          darkgray: 11119017,
          darkgreen: 25600,
          darkgrey: 11119017,
          darkkhaki: 12433259,
          darkmagenta: 9109643,
          darkolivegreen: 5597999,
          darkorange: 16747520,
          darkorchid: 10040012,
          darkred: 9109504,
          darksalmon: 15308410,
          darkseagreen: 9419919,
          darkslateblue: 4734347,
          darkslategray: 3100495,
          darkslategrey: 3100495,
          darkturquoise: 52945,
          darkviolet: 9699539,
          deeppink: 16716947,
          deepskyblue: 49151,
          dimgray: 6908265,
          dimgrey: 6908265,
          dodgerblue: 2003199,
          firebrick: 11674146,
          floralwhite: 16775920,
          forestgreen: 2263842,
          fuchsia: 16711935,
          gainsboro: 14474460,
          ghostwhite: 16316671,
          gold: 16766720,
          goldenrod: 14329120,
          gray: 8421504,
          green: 32768,
          greenyellow: 11403055,
          grey: 8421504,
          honeydew: 15794160,
          hotpink: 16738740,
          indianred: 13458524,
          indigo: 4915330,
          ivory: 16777200,
          khaki: 15787660,
          lavender: 15132410,
          lavenderblush: 16773365,
          lawngreen: 8190976,
          lemonchiffon: 16775885,
          lightblue: 11393254,
          lightcoral: 15761536,
          lightcyan: 14745599,
          lightgoldenrodyellow: 16448210,
          lightgray: 13882323,
          lightgreen: 9498256,
          lightgrey: 13882323,
          lightpink: 16758465,
          lightsalmon: 16752762,
          lightseagreen: 2142890,
          lightskyblue: 8900346,
          lightslategray: 7833753,
          lightslategrey: 7833753,
          lightsteelblue: 11584734,
          lightyellow: 16777184,
          lime: 65280,
          limegreen: 3329330,
          linen: 16445670,
          magenta: 16711935,
          maroon: 8388608,
          mediumaquamarine: 6737322,
          mediumblue: 205,
          mediumorchid: 12211667,
          mediumpurple: 9662683,
          mediumseagreen: 3978097,
          mediumslateblue: 8087790,
          mediumspringgreen: 64154,
          mediumturquoise: 4772300,
          mediumvioletred: 13047173,
          midnightblue: 1644912,
          mintcream: 16121850,
          mistyrose: 16770273,
          moccasin: 16770229,
          navajowhite: 16768685,
          navy: 128,
          oldlace: 16643558,
          olive: 8421376,
          olivedrab: 7048739,
          orange: 16753920,
          orangered: 16729344,
          orchid: 14315734,
          palegoldenrod: 15657130,
          palegreen: 10025880,
          paleturquoise: 11529966,
          palevioletred: 14381203,
          papayawhip: 16773077,
          peachpuff: 16767673,
          peru: 13468991,
          pink: 16761035,
          plum: 14524637,
          powderblue: 11591910,
          purple: 8388736,
          rebeccapurple: 6697881,
          red: 16711680,
          rosybrown: 12357519,
          royalblue: 4286945,
          saddlebrown: 9127187,
          salmon: 16416882,
          sandybrown: 16032864,
          seagreen: 3050327,
          seashell: 16774638,
          sienna: 10506797,
          silver: 12632256,
          skyblue: 8900331,
          slateblue: 6970061,
          slategray: 7372944,
          slategrey: 7372944,
          snow: 16775930,
          springgreen: 65407,
          steelblue: 4620980,
          tan: 13808780,
          teal: 32896,
          thistle: 14204888,
          tomato: 16737095,
          turquoise: 4251856,
          violet: 15631086,
          wheat: 16113331,
          white: 16777215,
          whitesmoke: 16119285,
          yellow: 16776960,
          yellowgreen: 10145074,
        };
      function b() {
        return this.rgb().formatHex();
      }
      function x() {
        return this.rgb().formatRgb();
      }
      function O(t) {
        var e, n;
        return (
          (t = (t + "").trim().toLowerCase()),
          (e = f.exec(t))
            ? ((n = e[1].length),
              (e = parseInt(e[1], 16)),
              6 === n
                ? w(e)
                : 3 === n
                  ? new A(
                      ((e >> 8) & 15) | ((e >> 4) & 240),
                      ((e >> 4) & 15) | (240 & e),
                      ((15 & e) << 4) | (15 & e),
                      1,
                    )
                  : 8 === n
                    ? C(
                        (e >> 24) & 255,
                        (e >> 16) & 255,
                        (e >> 8) & 255,
                        (255 & e) / 255,
                      )
                    : 4 === n
                      ? C(
                          ((e >> 12) & 15) | ((e >> 8) & 240),
                          ((e >> 8) & 15) | ((e >> 4) & 240),
                          ((e >> 4) & 15) | (240 & e),
                          (((15 & e) << 4) | (15 & e)) / 255,
                        )
                      : null)
            : (e = p.exec(t))
              ? new A(e[1], e[2], e[3], 1)
              : (e = d.exec(t))
                ? new A(
                    (255 * e[1]) / 100,
                    (255 * e[2]) / 100,
                    (255 * e[3]) / 100,
                    1,
                  )
                : (e = h.exec(t))
                  ? C(e[1], e[2], e[3], e[4])
                  : (e = v.exec(t))
                    ? C(
                        (255 * e[1]) / 100,
                        (255 * e[2]) / 100,
                        (255 * e[3]) / 100,
                        e[4],
                      )
                    : (e = y.exec(t))
                      ? T(e[1], e[2] / 100, e[3] / 100, 1)
                      : (e = m.exec(t))
                        ? T(e[1], e[2] / 100, e[3] / 100, e[4])
                        : g.hasOwnProperty(t)
                          ? w(g[t])
                          : "transparent" === t
                            ? new A(NaN, NaN, NaN, 0)
                            : null
        );
      }
      function w(t) {
        return new A((t >> 16) & 255, (t >> 8) & 255, 255 & t, 1);
      }
      function C(t, e, n, r) {
        return r <= 0 && (t = e = n = NaN), new A(t, e, n, r);
      }
      function S(t, e, n, r) {
        return 1 === arguments.length
          ? ((o = t) instanceof a || (o = O(o)),
            o ? new A((o = o.rgb()).r, o.g, o.b, o.opacity) : new A())
          : new A(t, e, n, null == r ? 1 : r);
        var o;
      }
      function A(t, e, n, r) {
        (this.r = +t), (this.g = +e), (this.b = +n), (this.opacity = +r);
      }
      function j() {
        return "#".concat(M(this.r)).concat(M(this.g)).concat(M(this.b));
      }
      function k() {
        const t = P(this.opacity);
        return ""
          .concat(1 === t ? "rgb(" : "rgba(")
          .concat(E(this.r), ", ")
          .concat(E(this.g), ", ")
          .concat(E(this.b))
          .concat(1 === t ? ")" : ", ".concat(t, ")"));
      }
      function P(t) {
        return isNaN(t) ? 1 : Math.max(0, Math.min(1, t));
      }
      function E(t) {
        return Math.max(0, Math.min(255, Math.round(t) || 0));
      }
      function M(t) {
        return ((t = E(t)) < 16 ? "0" : "") + t.toString(16);
      }
      function T(t, e, n, r) {
        return (
          r <= 0
            ? (t = e = n = NaN)
            : n <= 0 || n >= 1
              ? (t = e = NaN)
              : e <= 0 && (t = NaN),
          new L(t, e, n, r)
        );
      }
      function _(t) {
        if (t instanceof L) return new L(t.h, t.s, t.l, t.opacity);
        if ((t instanceof a || (t = O(t)), !t)) return new L();
        if (t instanceof L) return t;
        var e = (t = t.rgb()).r / 255,
          n = t.g / 255,
          r = t.b / 255,
          o = Math.min(e, n, r),
          i = Math.max(e, n, r),
          c = NaN,
          l = i - o,
          u = (i + o) / 2;
        return (
          l
            ? ((c =
                e === i
                  ? (n - r) / l + 6 * (n < r)
                  : n === i
                    ? (r - e) / l + 2
                    : (e - n) / l + 4),
              (l /= u < 0.5 ? i + o : 2 - i - o),
              (c *= 60))
            : (l = u > 0 && u < 1 ? 0 : c),
          new L(c, l, u, t.opacity)
        );
      }
      function L(t, e, n, r) {
        (this.h = +t), (this.s = +e), (this.l = +n), (this.opacity = +r);
      }
      function D(t) {
        return (t = (t || 0) % 360) < 0 ? t + 360 : t;
      }
      function I(t) {
        return Math.max(0, Math.min(1, t || 0));
      }
      function R(t, e, n) {
        return (
          255 *
          (t < 60
            ? e + ((n - e) * t) / 60
            : t < 180
              ? n
              : t < 240
                ? e + ((n - e) * (240 - t)) / 60
                : e)
        );
      }
      function N(t, e, n, r, o) {
        var a = t * t,
          i = a * t;
        return (
          ((1 - 3 * t + 3 * a - i) * e +
            (4 - 6 * a + 3 * i) * n +
            (1 + 3 * t + 3 * a - 3 * i) * r +
            i * o) /
          6
        );
      }
      r(a, O, {
        copy(t) {
          return Object.assign(new this.constructor(), this, t);
        },
        displayable() {
          return this.rgb().displayable();
        },
        hex: b,
        formatHex: b,
        formatHex8: function () {
          return this.rgb().formatHex8();
        },
        formatHsl: function () {
          return _(this).formatHsl();
        },
        formatRgb: x,
        toString: x,
      }),
        r(
          A,
          S,
          o(a, {
            brighter(t) {
              return (
                (t = null == t ? c : Math.pow(c, t)),
                new A(this.r * t, this.g * t, this.b * t, this.opacity)
              );
            },
            darker(t) {
              return (
                (t = null == t ? i : Math.pow(i, t)),
                new A(this.r * t, this.g * t, this.b * t, this.opacity)
              );
            },
            rgb() {
              return this;
            },
            clamp() {
              return new A(E(this.r), E(this.g), E(this.b), P(this.opacity));
            },
            displayable() {
              return (
                -0.5 <= this.r &&
                this.r < 255.5 &&
                -0.5 <= this.g &&
                this.g < 255.5 &&
                -0.5 <= this.b &&
                this.b < 255.5 &&
                0 <= this.opacity &&
                this.opacity <= 1
              );
            },
            hex: j,
            formatHex: j,
            formatHex8: function () {
              return "#"
                .concat(M(this.r))
                .concat(M(this.g))
                .concat(M(this.b))
                .concat(M(255 * (isNaN(this.opacity) ? 1 : this.opacity)));
            },
            formatRgb: k,
            toString: k,
          }),
        ),
        r(
          L,
          function (t, e, n, r) {
            return 1 === arguments.length
              ? _(t)
              : new L(t, e, n, null == r ? 1 : r);
          },
          o(a, {
            brighter(t) {
              return (
                (t = null == t ? c : Math.pow(c, t)),
                new L(this.h, this.s, this.l * t, this.opacity)
              );
            },
            darker(t) {
              return (
                (t = null == t ? i : Math.pow(i, t)),
                new L(this.h, this.s, this.l * t, this.opacity)
              );
            },
            rgb() {
              var t = (this.h % 360) + 360 * (this.h < 0),
                e = isNaN(t) || isNaN(this.s) ? 0 : this.s,
                n = this.l,
                r = n + (n < 0.5 ? n : 1 - n) * e,
                o = 2 * n - r;
              return new A(
                R(t >= 240 ? t - 240 : t + 120, o, r),
                R(t, o, r),
                R(t < 120 ? t + 240 : t - 120, o, r),
                this.opacity,
              );
            },
            clamp() {
              return new L(D(this.h), I(this.s), I(this.l), P(this.opacity));
            },
            displayable() {
              return (
                ((0 <= this.s && this.s <= 1) || isNaN(this.s)) &&
                0 <= this.l &&
                this.l <= 1 &&
                0 <= this.opacity &&
                this.opacity <= 1
              );
            },
            formatHsl() {
              const t = P(this.opacity);
              return ""
                .concat(1 === t ? "hsl(" : "hsla(")
                .concat(D(this.h), ", ")
                .concat(100 * I(this.s), "%, ")
                .concat(100 * I(this.l), "%")
                .concat(1 === t ? ")" : ", ".concat(t, ")"));
            },
          }),
        );
      const W = (t) => () => t;
      function F(t, e) {
        return function (n) {
          return t + n * e;
        };
      }
      function z(t) {
        return 1 === (t = +t)
          ? U
          : function (e, n) {
              return n - e
                ? (function (t, e, n) {
                    return (
                      (t = Math.pow(t, n)),
                      (e = Math.pow(e, n) - t),
                      (n = 1 / n),
                      function (r) {
                        return Math.pow(t + r * e, n);
                      }
                    );
                  })(e, n, t)
                : W(isNaN(e) ? n : e);
            };
      }
      function U(t, e) {
        var n = e - t;
        return n ? F(t, n) : W(isNaN(t) ? e : t);
      }
      const B = (function t(e) {
        var n = z(e);
        function r(t, e) {
          var r = n((t = S(t)).r, (e = S(e)).r),
            o = n(t.g, e.g),
            a = n(t.b, e.b),
            i = U(t.opacity, e.opacity);
          return function (e) {
            return (
              (t.r = r(e)),
              (t.g = o(e)),
              (t.b = a(e)),
              (t.opacity = i(e)),
              t + ""
            );
          };
        }
        return (r.gamma = t), r;
      })(1);
      function q(t) {
        return function (e) {
          var n,
            r,
            o = e.length,
            a = new Array(o),
            i = new Array(o),
            c = new Array(o);
          for (n = 0; n < o; ++n)
            (r = S(e[n])),
              (a[n] = r.r || 0),
              (i[n] = r.g || 0),
              (c[n] = r.b || 0);
          return (
            (a = t(a)),
            (i = t(i)),
            (c = t(c)),
            (r.opacity = 1),
            function (t) {
              return (r.r = a(t)), (r.g = i(t)), (r.b = c(t)), r + "";
            }
          );
        };
      }
      q(function (t) {
        var e = t.length - 1;
        return function (n) {
          var r =
              n <= 0 ? (n = 0) : n >= 1 ? ((n = 1), e - 1) : Math.floor(n * e),
            o = t[r],
            a = t[r + 1],
            i = r > 0 ? t[r - 1] : 2 * o - a,
            c = r < e - 1 ? t[r + 2] : 2 * a - o;
          return N((n - r / e) * e, i, o, a, c);
        };
      }),
        q(function (t) {
          var e = t.length;
          return function (n) {
            var r = Math.floor(((n %= 1) < 0 ? ++n : n) * e),
              o = t[(r + e - 1) % e],
              a = t[r % e],
              i = t[(r + 1) % e],
              c = t[(r + 2) % e];
            return N((n - r / e) * e, o, a, i, c);
          };
        });
      function H(t, e) {
        var n,
          r = e ? e.length : 0,
          o = t ? Math.min(r, t.length) : 0,
          a = new Array(o),
          i = new Array(r);
        for (n = 0; n < o; ++n) a[n] = Q(t[n], e[n]);
        for (; n < r; ++n) i[n] = e[n];
        return function (t) {
          for (n = 0; n < o; ++n) i[n] = a[n](t);
          return i;
        };
      }
      function V(t, e) {
        var n = new Date();
        return (
          (t = +t),
          (e = +e),
          function (r) {
            return n.setTime(t * (1 - r) + e * r), n;
          }
        );
      }
      var $ = n(14837);
      function Y(t, e) {
        var n,
          r = {},
          o = {};
        for (n in ((null !== t && "object" === typeof t) || (t = {}),
        (null !== e && "object" === typeof e) || (e = {}),
        e))
          n in t ? (r[n] = Q(t[n], e[n])) : (o[n] = e[n]);
        return function (t) {
          for (n in r) o[n] = r[n](t);
          return o;
        };
      }
      var Z = /[-+]?(?:\d+\.?\d*|\.?\d+)(?:[eE][-+]?\d+)?/g,
        K = new RegExp(Z.source, "g");
      function G(t, e) {
        var n,
          r,
          o,
          a = (Z.lastIndex = K.lastIndex = 0),
          i = -1,
          c = [],
          l = [];
        for (t += "", e += ""; (n = Z.exec(t)) && (r = K.exec(e)); )
          (o = r.index) > a &&
            ((o = e.slice(a, o)), c[i] ? (c[i] += o) : (c[++i] = o)),
            (n = n[0]) === (r = r[0])
              ? c[i]
                ? (c[i] += r)
                : (c[++i] = r)
              : ((c[++i] = null), l.push({ i: i, x: (0, $.Z)(n, r) })),
            (a = K.lastIndex);
        return (
          a < e.length && ((o = e.slice(a)), c[i] ? (c[i] += o) : (c[++i] = o)),
          c.length < 2
            ? l[0]
              ? (function (t) {
                  return function (e) {
                    return t(e) + "";
                  };
                })(l[0].x)
              : (function (t) {
                  return function () {
                    return t;
                  };
                })(e)
            : ((e = l.length),
              function (t) {
                for (var n, r = 0; r < e; ++r) c[(n = l[r]).i] = n.x(t);
                return c.join("");
              })
        );
      }
      function X(t, e) {
        e || (e = []);
        var n,
          r = t ? Math.min(e.length, t.length) : 0,
          o = e.slice();
        return function (a) {
          for (n = 0; n < r; ++n) o[n] = t[n] * (1 - a) + e[n] * a;
          return o;
        };
      }
      function Q(t, e) {
        var n,
          r,
          o = typeof e;
        return null == e || "boolean" === o
          ? W(e)
          : ("number" === o
              ? $.Z
              : "string" === o
                ? (n = O(e))
                  ? ((e = n), B)
                  : G
                : e instanceof O
                  ? B
                  : e instanceof Date
                    ? V
                    : ((r = e),
                      !ArrayBuffer.isView(r) || r instanceof DataView
                        ? Array.isArray(e)
                          ? H
                          : ("function" !== typeof e.valueOf &&
                                "function" !== typeof e.toString) ||
                              isNaN(e)
                            ? Y
                            : $.Z
                        : X))(t, e);
      }
    },
  },
]);
//# sourceMappingURL=274.c892ae50.chunk.js.map
