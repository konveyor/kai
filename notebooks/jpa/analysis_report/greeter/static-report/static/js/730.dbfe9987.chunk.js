"use strict";
(self.webpackChunkkonveyor_static_report =
  self.webpackChunkkonveyor_static_report || []).push([
  [730],
  {
    85029: (t, e, n) => {
      n.r(e), n.d(e, { default: () => _ });
      var r = n(72791),
        s = n(16871),
        o = n(27054),
        i = n(20738),
        c = n(86896),
        l = n(55197),
        a = n(87296),
        d = n(4464),
        h = n(54149),
        x = n(5291),
        j = n(3782),
        y = n(34022),
        g = n(21709),
        p = n(38625),
        u = n(66872),
        m = n(41262),
        P = n(49384),
        T = n(6964),
        I = n(86257),
        f = n(70730),
        S = n(70494),
        b = n(7155),
        k = n(88473),
        C = n(80184);
      const v = k.ZV.map((t) => ({
          category: t,
          totalIncidents: 0,
          totalStoryPoints: 0,
        })),
        w = {
          IncidentsBar: {
            getY: (t) => t.totalIncidents,
            getTooltip: (t) => {
              let { datum: e } = t;
              return "".concat(e.y, " incidents");
            },
          },
          StoryPointsBar: {
            getY: (t) => t.totalStoryPoints,
            getTooltip: (t) => {
              let { datum: e } = t;
              return "".concat(e.y, " SP");
            },
          },
        },
        B = (t) => {
          let { application: e } = t;
          const n = e.issues,
            s = (0, r.useMemo)(
              () =>
                (n || []).reduce((t, e) => {
                  const n = t.find((t) => t.category === e.category);
                  let r;
                  return (
                    (r = n
                      ? [
                          ...t.filter((t) => t.category !== e.category),
                          {
                            category: e.category,
                            totalIncidents: n.totalIncidents + e.totalIncidents,
                            totalStoryPoints:
                              n.totalStoryPoints + e.totalEffort,
                          },
                        ]
                      : [
                          ...t,
                          {
                            category: e.category,
                            totalIncidents: 0,
                            totalStoryPoints: 0,
                          },
                        ]),
                    r.sort((0, k.BM)((t) => t.category))
                  );
                }, v),
              [n],
            );
          return (0, C.jsxs)(y.r, {
            md: 6,
            children: [
              (0, C.jsx)(g.P, {
                children: (0, C.jsxs)(p.Z, {
                  isFullHeight: !0,
                  children: [
                    (0, C.jsx)(u.l, { children: "Incidents" }),
                    (0, C.jsx)(m.e, {
                      children: (0, C.jsxs)(P.i, {
                        variant: "compact",
                        children: [
                          (0, C.jsx)(T.h, {
                            children: (0, C.jsxs)(I.Tr, {
                              children: [
                                (0, C.jsx)(f.Th, {
                                  width: 40,
                                  children: "Category",
                                }),
                                (0, C.jsx)(f.Th, { children: "Incidents" }),
                                (0, C.jsx)(f.Th, {
                                  children: "Total Story Points",
                                }),
                              ],
                            }),
                          }),
                          (0, C.jsx)(S.p, {
                            children: s.map((t) =>
                              (0, C.jsxs)(
                                I.Tr,
                                {
                                  children: [
                                    (0, C.jsx)(b.Td, { children: t.category }),
                                    (0, C.jsx)(b.Td, {
                                      children: t.totalIncidents,
                                    }),
                                    (0, C.jsx)(b.Td, {
                                      children: t.totalStoryPoints,
                                    }),
                                  ],
                                },
                                t.category,
                              ),
                            ),
                          }),
                        ],
                      }),
                    }),
                  ],
                }),
              }),
              (0, C.jsx)(g.P, {
                children: (0, C.jsxs)(p.Z, {
                  isFullHeight: !0,
                  children: [
                    (0, C.jsx)(u.l, { children: "Incidents and Story Points" }),
                    (0, C.jsx)(m.e, {
                      children: (0, C.jsxs)(l.k, {
                        themeColor: a.n.multiOrdered,
                        domainPadding: { x: 35 },
                        padding: { bottom: 40, top: 20, left: 60, right: 0 },
                        height: 300,
                        width: 700,
                        children: [
                          (0, C.jsx)(d.C, {}),
                          (0, C.jsx)(d.C, { dependentAxis: !0, showGrid: !1 }),
                          (0, C.jsx)(h.G, {
                            offset: 10,
                            children: Object.entries(w).map((t) => {
                              let [e, n] = t;
                              return (0, C.jsx)(
                                x.B,
                                {
                                  data: s.map((t) => ({
                                    name: e,
                                    x: t.category,
                                    y: n.getY(t),
                                    label: n.getTooltip,
                                  })),
                                  labelComponent: (0, C.jsx)(j.h, {
                                    constrainToVisibleArea: !0,
                                  }),
                                },
                                e,
                              );
                            }),
                          }),
                        ],
                      }),
                    }),
                  ],
                }),
              }),
            ],
          });
        },
        _ = () => {
          const t = (0, s.bx)();
          return (0, C.jsx)(C.Fragment, {
            children: (0, C.jsx)(o.NP, {
              children: (0, C.jsx)(i.K, {
                hasGutter: !0,
                children: (0, C.jsx)(c.v, {
                  children: t && (0, C.jsx)(B, { application: t }),
                }),
              }),
            }),
          });
        };
    },
  },
]);
//# sourceMappingURL=730.dbfe9987.chunk.js.map
