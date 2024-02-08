"use strict";
(self.webpackChunkkonveyor_static_report =
  self.webpackChunkkonveyor_static_report || []).push([
  [600],
  {
    64600: (e, a, i) => {
      i.r(a), i.d(a, { default: () => S });
      var t = i(72791),
        r = i(16871),
        n = i(43504),
        l = i(27054),
        s = i(75971);
      const o = "pf-v5-c-breadcrumb",
        d = "pf-v5-c-breadcrumb__dropdown",
        c = "pf-v5-c-breadcrumb__item",
        m = "pf-v5-c-breadcrumb__item-divider",
        p = "pf-v5-c-breadcrumb__link",
        u = "pf-v5-c-breadcrumb__list",
        v = { current: "pf-m-current" };
      var h = i(31994),
        b = i(44134);
      const f = (e) => {
        var {
            children: a = null,
            className: i = "",
            "aria-label": r = "Breadcrumb",
            ouiaId: n,
            ouiaSafe: l = !0,
          } = e,
          d = (0, s.__rest)(e, [
            "children",
            "className",
            "aria-label",
            "ouiaId",
            "ouiaSafe",
          ]);
        const c = (0, b.S$)(f.displayName, n, l);
        return t.createElement(
          "nav",
          Object.assign(
            {},
            d,
            { "aria-label": r, className: (0, h.i)(o, i) },
            c,
          ),
          t.createElement(
            "ol",
            { className: u, role: "list" },
            t.Children.map(a, (e, a) => {
              const i = a > 0;
              return t.isValidElement(e)
                ? t.cloneElement(e, { showDivider: i })
                : e;
            }),
          ),
        );
      };
      f.displayName = "Breadcrumb";
      var g = i(32994);
      const N = (e) => {
        var {
            children: a = null,
            className: i = "",
            to: r,
            isActive: n = !1,
            isDropdown: l = !1,
            showDivider: o,
            target: u,
            component: b = "a",
            render: f,
          } = e,
          N = (0, s.__rest)(e, [
            "children",
            "className",
            "to",
            "isActive",
            "isDropdown",
            "showDivider",
            "target",
            "component",
            "render",
          ]);
        const w = b,
          k = n ? "page" : void 0,
          _ = (0, h.i)(p, n && v.current);
        return t.createElement(
          "li",
          Object.assign({}, N, { className: (0, h.i)(c, i) }),
          o &&
            t.createElement(
              "span",
              { className: m },
              t.createElement(g.ZP, null),
            ),
          "button" === b &&
            t.createElement(
              "button",
              { className: _, "aria-current": k, type: "button" },
              a,
            ),
          l && t.createElement("span", { className: (0, h.i)(d) }, a),
          f && f({ className: _, ariaCurrent: k }),
          r &&
            !f &&
            t.createElement(
              w,
              { href: r, target: u, className: _, "aria-current": k },
              a,
            ),
          !r && "button" !== b && !l && a,
        );
      };
      N.displayName = "BreadcrumbItem";
      var w = i(17300),
        k = i(45145),
        _ = i(53894),
        Z = i(32352),
        j = i(198),
        x = i(76925),
        y = i(80184);
      const S = () => {
        var e;
        const a = (0, r.s0)(),
          i = (0, r.TH)(),
          s = (0, r.bS)("/applications/:applicationId/*"),
          o = (0, x.Le)(),
          d = (0, t.useMemo)(() => {
            var e;
            const a =
              null === s || void 0 === s ? void 0 : s.params.applicationId;
            return (
              (null === (e = o.data) || void 0 === e
                ? void 0
                : e.find((e) => e.id === a)) || null
            );
          }, [null === s || void 0 === s ? void 0 : s.params, o.data]),
          c = (0, t.useMemo)(
            () => [
              {
                title: "Dashboard",
                path: "/applications/".concat(
                  null === d || void 0 === d ? void 0 : d.id,
                  "/dashboard",
                ),
              },
              {
                title: "Issues",
                path: "/applications/".concat(
                  null === d || void 0 === d ? void 0 : d.id,
                  "/issues",
                ),
              },
              {
                title: "Dependencies",
                path: "/applications/".concat(
                  null === d || void 0 === d ? void 0 : d.id,
                  "/dependencies",
                ),
              },
              {
                title: "Technologies",
                path: "/applications/".concat(
                  null === d || void 0 === d ? void 0 : d.id,
                  "/technologies",
                ),
              },
            ],
            [d],
          );
        return (0, y.jsxs)(y.Fragment, {
          children: [
            (0, y.jsx)(l.NP, {
              type: "breadcrumb",
              children: (0, y.jsxs)(f, {
                children: [
                  (0, y.jsx)(N, {
                    children: (0, y.jsx)(n.rU, {
                      to: "/applications",
                      children: "Applications",
                    }),
                  }),
                  (0, y.jsx)(N, {
                    isActive: !0,
                    children: null === d || void 0 === d ? void 0 : d.name,
                  }),
                ],
              }),
            }),
            (0, y.jsx)(l.NP, {
              type: "default",
              variant: "light",
              children: (0, y.jsx)(w.D, {
                children: (0, y.jsx)(k.x, {
                  component: "h1",
                  children: null === d || void 0 === d ? void 0 : d.name,
                }),
              }),
            }),
            (0, y.jsx)(l.NP, {
              type: "tabs",
              variant: "light",
              children: (0, y.jsx)(_.m, {
                role: "region",
                activeKey:
                  null === (e = c.find((e) => e.path === i.pathname)) ||
                  void 0 === e
                    ? void 0
                    : e.path,
                onSelect: (e, i) => a("".concat(i)),
                isOverflowHorizontal: { showTabCount: !0 },
                children: c.map((e, a) =>
                  (0, y.jsx)(
                    Z.O,
                    {
                      eventKey: e.path,
                      title: (0, y.jsx)(j.T, { children: e.title }),
                    },
                    a,
                  ),
                ),
              }),
            }),
            (0, y.jsx)(r.j3, { context: d }),
          ],
        });
      };
    },
    27054: (e, a, i) => {
      i.d(a, { Dk: () => t, NP: () => u });
      var t,
        r,
        n = i(75971),
        l = i(72791),
        s = i(64843),
        o = i(31994),
        d = i(31677),
        c = i(87149);
      !(function (e) {
        (e.default = "default"),
          (e.light = "light"),
          (e.dark = "dark"),
          (e.darker = "darker");
      })(t || (t = {})),
        (function (e) {
          (e.default = "default"),
            (e.nav = "nav"),
            (e.subNav = "subnav"),
            (e.breadcrumb = "breadcrumb"),
            (e.tabs = "tabs"),
            (e.wizard = "wizard");
        })(r || (r = {}));
      const m = {
          [r.default]: s.Z.pageMainSection,
          [r.nav]: s.Z.pageMainNav,
          [r.subNav]: s.Z.pageMainSubnav,
          [r.breadcrumb]: s.Z.pageMainBreadcrumb,
          [r.tabs]: s.Z.pageMainTabs,
          [r.wizard]: s.Z.pageMainWizard,
        },
        p = {
          [t.default]: "",
          [t.light]: s.Z.modifiers.light,
          [t.dark]: s.Z.modifiers.dark_200,
          [t.darker]: s.Z.modifiers.dark_100,
        },
        u = (e) => {
          var {
              className: a = "",
              children: i,
              variant: t = "default",
              type: u = "default",
              padding: v,
              isFilled: h,
              isWidthLimited: b = !1,
              isCenterAligned: f = !1,
              stickyOnBreakpoint: g,
              hasShadowTop: N = !1,
              hasShadowBottom: w = !1,
              hasOverflowScroll: k = !1,
              "aria-label": _,
              component: Z = "section",
            } = e,
            j = (0, n.__rest)(e, [
              "className",
              "children",
              "variant",
              "type",
              "padding",
              "isFilled",
              "isWidthLimited",
              "isCenterAligned",
              "stickyOnBreakpoint",
              "hasShadowTop",
              "hasShadowBottom",
              "hasOverflowScroll",
              "aria-label",
              "component",
            ]);
          const { height: x, getVerticalBreakpoint: y } = l.useContext(c.z1);
          l.useEffect(() => {
            k &&
              !_ &&
              console.warn(
                "PageSection: An accessible aria-label is required when hasOverflowScroll is set to true.",
              );
          }, [k, _]);
          const S = Z;
          return l.createElement(
            S,
            Object.assign(
              {},
              j,
              {
                className: (0, o.i)(
                  m[u],
                  (0, d.wt)(v, s.Z),
                  (0, d.wt)(g, s.Z, "sticky-", y(x), !0),
                  p[t],
                  !1 === h && s.Z.modifiers.noFill,
                  !0 === h && s.Z.modifiers.fill,
                  b && s.Z.modifiers.limitWidth,
                  b && f && u !== r.subNav && s.Z.modifiers.alignCenter,
                  N && s.Z.modifiers.shadowTop,
                  w && s.Z.modifiers.shadowBottom,
                  k && s.Z.modifiers.overflowScroll,
                  a,
                ),
              },
              k && { tabIndex: 0 },
              { "aria-label": _ },
            ),
            b &&
              l.createElement(
                "div",
                { className: (0, o.i)(s.Z.pageMainBody) },
                i,
              ),
            !b && i,
          );
        };
      u.displayName = "PageSection";
    },
  },
]);
//# sourceMappingURL=600.f15ec235.chunk.js.map
