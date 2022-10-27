/*!
* jquery.inputmask.bundle.js
* https://github.com/RobinHerbots/jquery.inputmask
* Copyright (c) 2010 - 2016 Robin Herbots
* Licensed under the MIT license (http://www.opensource.org/licenses/mit-license.php)
* Version: 3.3.4-18
*/
!function(a) {
	function b(c, d) {
		return this instanceof b ? (a.isPlainObject(c) ? d = c : (d = d || {}, d.alias = c), this.el = void 0, this.opts = a.extend(!0, {}, this.defaults, d), this.noMasksCache = d && void 0 !== d.definitions, this.userOptions = d || {}, this.events = {}, void e(this.opts.alias, d, this.opts)) : new b(c, d)
	}
	function c(a) {
		var b = document.createElement("input"),
			c = "on" + a,
			d = c in b;
		return d || (b.setAttribute(c, "return;"), d = "function" == typeof b[c]), b = null, d
	}
	function d(b, c) {
		var d = b.getAttribute("type"),
			e = "INPUT" === b.tagName && a.inArray(d, c.supportsInputType) !== -1 || b.isContentEditable || "TEXTAREA" === b.tagName;
		if (!e && "INPUT" === b.tagName) {
			var f = document.createElement("input");
			f.setAttribute("type", d),
			e = "text" === f.type,
			f = null
		}
		return e
	}
	function e(b, c, d) {
		var f = d.aliases[b];
		return f ? (f.alias && e(f.alias, void 0, d), a.extend(!0, d, f), a.extend(!0, d, c), !0) : (null === d.mask && (d.mask = b), !1)
	}
	function f(b, c, d) {
		function f(a, c) {
			c = void 0 !== c ? c : b.getAttribute("data-inputmask-" + a),
			null !== c && ("string" == typeof c && (0 === a.indexOf("on") ? c = window[c] : "false" === c ? c = !1 : "true" === c && (c = !0)), d[a] = c)
		}
		var g,
			h,
			i,
			j,
			k = b.getAttribute("data-inputmask");
		if (k && "" !== k && (k = k.replace(new RegExp("'", "g"), '"'), h = JSON.parse("{" + k + "}")), h) {
			i = void 0;
			for (j in h)
				if ("alias" === j.toLowerCase()) {
					i = h[j];
					break
				}
		}
		f("alias", i),
		d.alias && e(d.alias, d, c);
		for (g in c) {
			if (h) {
				i = void 0;
				for (j in h)
					if (j.toLowerCase() === g.toLowerCase()) {
						i = h[j];
						break
					}
			}
			f(g, i)
		}
		return a.extend(!0, c, d), c
	}
	function g(c, d) {
		function e(b) {
			function d(a, b, c, d) {
				this.matches = [],
				this.isGroup = a || !1,
				this.isOptional = b || !1,
				this.isQuantifier = c || !1,
				this.isAlternator = d || !1,
				this.quantifier = {
					min: 1,
					max: 1
				}
			}
			function e(b, d, e) {
				var f = c.definitions[d];
				e = void 0 !== e ? e : b.matches.length;
				var g = b.matches[e - 1];
				if (f && !r) {
					f.placeholder = a.isFunction(f.placeholder) ? f.placeholder(c) : f.placeholder;
					for (var h = f.prevalidator, i = h ? h.length : 0, j = 1; j < f.cardinality; j++) {
						var k = i >= j ? h[j - 1] : [],
							l = k.validator,
							m = k.cardinality;
						b.matches.splice(e++, 0, {
							fn: l ? "string" == typeof l ? new RegExp(l) : new function() {
								this.test = l
							} : new RegExp("."),
							cardinality: m ? m : 1,
							optionality: b.isOptional,
							newBlockMarker: void 0 === g || g.def !== (f.definitionSymbol || d),
							casing: f.casing,
							def: f.definitionSymbol || d,
							placeholder: f.placeholder,
							mask: d
						}),
						g = b.matches[e - 1]
					}
					b.matches.splice(e++, 0, {
						fn: f.validator ? "string" == typeof f.validator ? new RegExp(f.validator) : new function() {
							this.test = f.validator
						} : new RegExp("."),
						cardinality: f.cardinality,
						optionality: b.isOptional,
						newBlockMarker: void 0 === g || g.def !== (f.definitionSymbol || d),
						casing: f.casing,
						def: f.definitionSymbol || d,
						placeholder: f.placeholder,
						mask: d
					})
				} else
					b.matches.splice(e++, 0, {
						fn: null,
						cardinality: 0,
						optionality: b.isOptional,
						newBlockMarker: void 0 === g || g.def !== d,
						casing: null,
						def: c.staticDefinitionSymbol || d,
						placeholder: void 0 !== c.staticDefinitionSymbol ? d : void 0,
						mask: d
					}),
					r = !1
			}
			function f(a, b) {
				a.isGroup && (a.isGroup = !1, e(a, c.groupmarker.start, 0), b !== !0 && e(a, c.groupmarker.end))
			}
			function g(a, b, c, d) {
				b.matches.length > 0 && (void 0 === d || d) && (c = b.matches[b.matches.length - 1], f(c)),
				e(b, a)
			}
			function h() {
				if (t.length > 0) {
					if (m = t[t.length - 1], g(k, m, o, !m.isAlternator), m.isAlternator) {
						n = t.pop();
						for (var a = 0; a < n.matches.length; a++)
							n.matches[a].isGroup = !1;
						t.length > 0 ? (m = t[t.length - 1], m.matches.push(n)) : s.matches.push(n)
					}
				} else
					g(k, s, o)
			}
			function i(a) {
				function b(a) {
					return a === c.optionalmarker.start ? a = c.optionalmarker.end : a === c.optionalmarker.end ? a = c.optionalmarker.start : a === c.groupmarker.start ? a = c.groupmarker.end : a === c.groupmarker.end && (a = c.groupmarker.start), a
				}
				a.matches = a.matches.reverse();
				for (var d in a.matches) {
					var e = parseInt(d);
					if (a.matches[d].isQuantifier && a.matches[e + 1] && a.matches[e + 1].isGroup) {
						var f = a.matches[d];
						a.matches.splice(d, 1),
						a.matches.splice(e + 1, 0, f)
					}
					void 0 !== a.matches[d].matches ? a.matches[d] = i(a.matches[d]) : a.matches[d] = b(a.matches[d])
				}
				return a
			}
			for (var j, k, l, m, n, o, p, q = /(?:[?*+]|\{[0-9\+\*]+(?:,[0-9\+\*]*)?\})|[^.?*+^${[]()|\\]+|./g, r = !1, s = new d, t = [], u = []; j = q.exec(b);)
				if (k = j[0], r)
					h();
				else
					switch (k.charAt(0)) {
					case c.escapeChar:
						r = !0;
						break;
					case c.optionalmarker.end:
					case c.groupmarker.end:
						if (l = t.pop(), void 0 !== l)
							if (t.length > 0) {
								if (m = t[t.length - 1], m.matches.push(l), m.isAlternator) {
									n = t.pop();
									for (var v = 0; v < n.matches.length; v++)
										n.matches[v].isGroup = !1;
									t.length > 0 ? (m = t[t.length - 1], m.matches.push(n)) : s.matches.push(n)
								}
							} else
								s.matches.push(l);
						else
							h();
						break;
					case c.optionalmarker.start:
						t.push(new d((!1), (!0)));
						break;
					case c.groupmarker.start:
						t.push(new d((!0)));
						break;
					case c.quantifiermarker.start:
						var w = new d((!1), (!1), (!0));
						k = k.replace(/[{}]/g, "");
						var x = k.split(","),
							y = isNaN(x[0]) ? x[0] : parseInt(x[0]),
							z = 1 === x.length ? y : isNaN(x[1]) ? x[1] : parseInt(x[1]);
						if ("*" !== z && "+" !== z || (y = "*" === z ? 0 : 1), w.quantifier = {
							min: y,
							max: z
						}, t.length > 0) {
							var A = t[t.length - 1].matches;
							j = A.pop(),
							j.isGroup || (p = new d((!0)), p.matches.push(j), j = p),
							A.push(j),
							A.push(w)
						} else
							j = s.matches.pop(),
							j.isGroup || (p = new d((!0)), p.matches.push(j), j = p),
							s.matches.push(j),
							s.matches.push(w);
						break;
					case c.alternatormarker:
						t.length > 0 ? (m = t[t.length - 1], o = m.matches.pop()) : o = s.matches.pop(),
						o.isAlternator ? t.push(o) : (n = new d((!1), (!1), (!1), (!0)), n.matches.push(o), t.push(n));
						break;
					default:
						h()
					}
			for (; t.length > 0;)
				l = t.pop(),
				f(l, !0),
				s.matches.push(l);
			return s.matches.length > 0 && (o = s.matches[s.matches.length - 1], f(o), u.push(s)), c.numericInput && i(u[0]), u
		}
		function f(f, g) {
			if (null !== f && "" !== f) {
				if (1 === f.length && c.greedy === !1 && 0 !== c.repeat && (c.placeholder = ""), c.repeat > 0 || "*" === c.repeat || "+" === c.repeat) {
					var h = "*" === c.repeat ? 0 : "+" === c.repeat ? 1 : c.repeat;
					f = c.groupmarker.start + f + c.groupmarker.end + c.quantifiermarker.start + h + "," + c.repeat + c.quantifiermarker.end
				}
				var i;
				return void 0 === b.prototype.masksCache[f] || d === !0 ? (i = {
					mask: f,
					maskToken: e(f),
					validPositions: {},
					_buffer: void 0,
					buffer: void 0,
					tests: {},
					metadata: g,
					maskLength: void 0
				}, d !== !0 && (b.prototype.masksCache[c.numericInput ? f.split("").reverse().join("") : f] = i, i = a.extend(!0, {}, b.prototype.masksCache[c.numericInput ? f.split("").reverse().join("") : f]))) : i = a.extend(!0, {}, b.prototype.masksCache[c.numericInput ? f.split("").reverse().join("") : f]), i
			}
		}
		function g(a) {
			return a = a.toString()
		}
		var h;
		if (a.isFunction(c.mask) && (c.mask = c.mask(c)), a.isArray(c.mask)) {
			if (c.mask.length > 1) {
				c.keepStatic = null === c.keepStatic || c.keepStatic;
				var i = "(";
				return a.each(c.numericInput ? c.mask.reverse() : c.mask, function(b, c) {
					i.length > 1 && (i += ")|("),
					i += g(void 0 === c.mask || a.isFunction(c.mask) ? c : c.mask)
				}), i += ")", f(i, c.mask)
			}
			c.mask = c.mask.pop()
		}
		return c.mask && (h = void 0 === c.mask.mask || a.isFunction(c.mask.mask) ? f(g(c.mask), c.mask) : f(g(c.mask.mask), c.mask)), h
	}
	function h(e, f, g) {
		function i(a, b, c) {
			b = b || 0;
			var d,
				e,
				f,
				h = [],
				i = 0,
				j = o();
			ga = void 0 !== ea ? ea.maxLength : void 0,
			ga === -1 && (ga = void 0);
			do {
				if (a === !0 && m().validPositions[i]) {
					var k = m().validPositions[i];
					e = k.match,
					d = k.locator.slice(),
					h.push(c === !0 ? k.input : H(i, e))
				} else
					f = r(i, d, i - 1),
					e = f.match,
					d = f.locator.slice(),
					(g.jitMasking === !1 || i < j || isFinite(g.jitMasking) && g.jitMasking > i) && h.push(H(i, e));
				i++
			} while ((void 0 === ga || i < ga) && (null !== e.fn || "" !== e.def) || b > i);
			return "" === h[h.length - 1] && h.pop(), m().maskLength = i + 1, h
		}
		function m() {
			return f
		}
		function n(a) {
			var b = m();
			b.buffer = void 0,
			a !== !0 && (b._buffer = void 0, b.validPositions = {}, b.p = 0)
		}
		function o(a, b, c) {
			var d = -1,
				e = -1,
				f = c || m().validPositions;
			void 0 === a && (a = -1);
			for (var g in f) {
				var h = parseInt(g);
				f[h] && (b || null !== f[h].match.fn) && (h <= a && (d = h), h >= a && (e = h))
			}
			return d !== -1 && a - d > 1 || e < a ? d : e
		}
		function p(b, c, d, e) {
			function f(a) {
				var b = m().validPositions[a];
				if (void 0 !== b && null === b.match.fn) {
					var c = m().validPositions[a - 1],
						d = m().validPositions[a + 1];
					return void 0 !== c && void 0 !== d
				}
				return !1
			}
			var h,
				i = b,
				j = a.extend(!0, {}, m().validPositions),
				k = !1;
			for (m().p = b, h = c - 1; h >= i; h--)
				void 0 !== m().validPositions[h] && (d === !0 || !f(h) && g.canClearPosition(m(), h, o(), e, g) !== !1) && delete m().validPositions[h];
			for (n(!0), h = i + 1; h <= o();) {
				for (; void 0 !== m().validPositions[i];)
					i++;
				var l = m().validPositions[i];
				if (h < i && (h = i + 1), void 0 === m().validPositions[h] && C(h) || void 0 !== l)
					h++;
				else {
					var p = r(h);
					k === !1 && j[i] && j[i].match.def === p.match.def ? (m().validPositions[i] = a.extend(!0, {}, j[i]), m().validPositions[i].input = p.input, delete m().validPositions[h], h++) : t(i, p.match.def) ? B(i, p.input || H(h), !0) !== !1 && (delete m().validPositions[h], h++, k = !0) : C(h) || (h++, i--),
					i++
				}
			}
			n(!0)
		}
		function q(a, b) {
			for (var c, d = a, e = o(), f = m().validPositions[e] || v(0)[0], h = void 0 !== f.alternation ? f.locator[f.alternation].toString().split(",") : [], i = 0; i < d.length && (c = d[i], !(c.match && (g.greedy && c.match.optionalQuantifier !== !0 || (c.match.optionality === !1 || c.match.newBlockMarker === !1) && c.match.optionalQuantifier !== !0) && (void 0 === f.alternation || f.alternation !== c.alternation || void 0 !== c.locator[f.alternation] && A(c.locator[f.alternation].toString().split(","), h))) || b === !0 && (null !== c.match.fn || /[0-9a-bA-Z]/.test(c.match.def))); i++)
				;
			return c
		}
		function r(a, b, c) {
			return m().validPositions[a] || q(v(a, b ? b.slice() : b, c))
		}
		function s(a) {
			return m().validPositions[a] ? m().validPositions[a] : v(a)[0]
		}
		function t(a, b) {
			for (var c = !1, d = v(a), e = 0; e < d.length; e++)
				if (d[e].match && d[e].match.def === b) {
					c = !0;
					break
				}
			return c
		}
		function u(b, c) {
			var d,
				e;
			return (m().tests[b] || m().validPositions[b]) && a.each(m().tests[b] || [m().validPositions[b]], function(a, b) {
				var f = b.alternation ? b.locator[b.alternation].toString().indexOf(c) : -1;
				(void 0 === e || f < e) && f !== -1 && (d = b, e = f)
			}), d
		}
		function v(b, c, d) {
			function e(c, d, f, h) {
				function j(f, h, l) {
					function q(b, c) {
						var d = 0 === a.inArray(b, c.matches);
						return d || a.each(c.matches, function(a, e) {
							if (e.isQuantifier === !0 && (d = q(b, c.matches[a - 1])))
								return !1
						}), d
					}
					function r(a, b) {
						var c = u(a, b);
						return c ? c.locator.slice(c.alternation + 1) : void 0
					}
					function s(a, c) {
						return null === a.match.fn && null !== c.match.fn && c.match.fn.test(a.match.def, m(), b, !1, g, !1)
					}
					if (k > 1e4)
						throw "Inputmask: There is probably an error in your mask definition or in the code. Create an issue on github with an example of the mask you are using. " + m().mask;
					if (k === b && void 0 === f.matches)
						return n.push({
							match: f,
							locator: h.reverse(),
							cd: p
						}), !0;
					if (void 0 !== f.matches) {
						if (f.isGroup && l !== f) {
							if (f = j(c.matches[a.inArray(f, c.matches) + 1], h))
								return !0
						} else if (f.isOptional) {
							var t = f;
							if (f = e(f, d, h, l)) {
								if (i = n[n.length - 1].match, !q(i, t))
									return !0;
								o = !0,
								k = b
							}
						} else if (f.isAlternator) {
							var v,
								w = f,
								x = [],
								y = n.slice(),
								z = h.length,
								A = d.length > 0 ? d.shift() : -1;
							if (A === -1 || "string" == typeof A) {
								var B,
									C = k,
									D = d.slice(),
									E = [];
								if ("string" == typeof A)
									E = A.split(",");
								else
									for (B = 0; B < w.matches.length; B++)
										E.push(B);
								for (var F = 0; F < E.length; F++) {
									if (B = parseInt(E[F]), n = [], d = r(k, B) || D.slice(), f = j(w.matches[B] || c.matches[B], [B].concat(h), l) || f, f !== !0 && void 0 !== f && E[E.length - 1] < w.matches.length) {
										var G = a.inArray(f, c.matches) + 1;
										c.matches.length > G && (f = j(c.matches[G], [G].concat(h.slice(1, h.length)), l), f && (E.push(G.toString()), a.each(n, function(a, b) {
											b.alternation = h.length - 1
										})))
									}
									v = n.slice(),
									k = C,
									n = [];
									for (var H = 0; H < v.length; H++) {
										var I = v[H],
											J = !1;
										I.alternation = I.alternation || z;
										for (var K = 0; K < x.length; K++) {
											var L = x[K];
											if (("string" != typeof A || a.inArray(I.locator[I.alternation].toString(), E) !== -1) && (I.match.def === L.match.def || s(I, L))) {
												J = I.match.mask === L.match.mask,
												L.locator[I.alternation].toString().indexOf(I.locator[I.alternation]) === -1 && (L.locator[I.alternation] = L.locator[I.alternation] + "," + I.locator[I.alternation], L.alternation = I.alternation, null == I.match.fn && (L.na = L.na || I.locator[I.alternation].toString(), L.na.indexOf(I.locator[I.alternation]) === -1 && (L.na = L.na + "," + I.locator[I.alternation])));
												break
											}
										}
										J || x.push(I)
									}
								}
								"string" == typeof A && (x = a.map(x, function(b, c) {
									if (isFinite(c)) {
										var d,
											e = b.alternation,
											f = b.locator[e].toString().split(",");
										b.locator[e] = void 0,
										b.alternation = void 0;
										for (var g = 0; g < f.length; g++)
											d = a.inArray(f[g], E) !== -1,
											d && (void 0 !== b.locator[e] ? (b.locator[e] += ",", b.locator[e] += f[g]) : b.locator[e] = parseInt(f[g]), b.alternation = e);
										if (void 0 !== b.locator[e])
											return b
									}
								})),
								n = y.concat(x),
								k = b,
								o = n.length > 0,
								d = D.slice()
							} else
								f = j(w.matches[A] || c.matches[A], [A].concat(h), l);
							if (f)
								return !0
						} else if (f.isQuantifier && l !== c.matches[a.inArray(f, c.matches) - 1])
							for (var M = f, N = d.length > 0 ? d.shift() : 0; N < (isNaN(M.quantifier.max) ? N + 1 : M.quantifier.max) && k <= b; N++) {
								var O = c.matches[a.inArray(M, c.matches) - 1];
								if (f = j(O, [N].concat(h), O)) {
									if (i = n[n.length - 1].match, i.optionalQuantifier = N > M.quantifier.min - 1, q(i, O)) {
										if (N > M.quantifier.min - 1) {
											o = !0,
											k = b;
											break
										}
										return !0
									}
									return !0
								}
							}
						else if (f = e(f, d, h, l))
							return !0
					} else
						k++
				}
				for (var l = d.length > 0 ? d.shift() : 0; l < c.matches.length; l++)
					if (c.matches[l].isQuantifier !== !0) {
						var q = j(c.matches[l], [l].concat(f), h);
						if (q && k === b)
							return q;
						if (k > b)
							break
					}
			}
			function f(b) {
				var c = [];
				return a.isArray(b) || (b = [b]), b.length > 0 && (void 0 === b[0].alternation ? (c = q(b.slice()).locator.slice(), 0 === c.length && (c = b[0].locator.slice())) : a.each(b, function(a, b) {
					if ("" !== b.def)
						if (0 === c.length)
							c = b.locator.slice();
						else
							for (var d = 0; d < c.length; d++)
								b.locator[d] && c[d].toString().indexOf(b.locator[d]) === -1 && (c[d] += "," + b.locator[d])
				})), c
			}
			function h(a) {
				return g.keepStatic && b > 0 && a.length > 1 + ("" === a[a.length - 1].match.def ? 1 : 0) && a[0].match.optionality !== !0 && a[0].match.optionalQuantifier !== !0 && null === a[0].match.fn && !/[0-9a-bA-Z]/.test(a[0].match.def) ? [q(a)] : a
			}
			var i,
				j = m().maskToken,
				k = c ? d : 0,
				l = c ? c.slice() : [0],
				n = [],
				o = !1,
				p = c ? c.join("") : "";
			if (b > -1) {
				if (void 0 === c) {
					for (var r, s = b - 1; void 0 === (r = m().validPositions[s] || m().tests[s]) && s > -1;)
						s--;
					void 0 !== r && s > -1 && (l = f(r), p = l.join(""), k = s)
				}
				if (m().tests[b] && m().tests[b][0].cd === p)
					return h(m().tests[b]);
				for (var t = l.shift(); t < j.length; t++) {
					var v = e(j[t], l, [t]);
					if (v && k === b || k > b)
						break
				}
			}
			return (0 === n.length || o) && n.push({
				match: {
					fn: null,
					cardinality: 0,
					optionality: !0,
					casing: null,
					def: "",
					placeholder: ""
				},
				locator: [],
				cd: p
			}), void 0 !== c && m().tests[b] ? h(a.extend(!0, [], n)) : (m().tests[b] = a.extend(!0, [], n), h(m().tests[b]))
		}
		function w() {
			return void 0 === m()._buffer && (m()._buffer = i(!1, 1), void 0 === m().buffer && m()._buffer.slice()), m()._buffer
		}
		function x(a) {
			return void 0 !== m().buffer && a !== !0 || (m().buffer = i(!0, o(), !0)), m().buffer
		}
		function y(a, b, c) {
			var d;
			if (a === !0)
				n(),
				a = 0,
				b = c.length;
			else
				for (d = a; d < b; d++)
					delete m().validPositions[d];
			for (d = a; d < b; d++)
				n(!0),
				c[d] !== g.skipOptionalPartCharacter && B(d, c[d], !0, !0)
		}
		function z(a, c, d) {
			switch (g.casing || c.casing) {
			case "upper":
				a = a.toUpperCase();
				break;
			case "lower":
				a = a.toLowerCase();
				break;
			case "title":
				var e = m().validPositions[d - 1];
				a = 0 === d || e && e.input === String.fromCharCode(b.keyCode.SPACE) ? a.toUpperCase() : a.toLowerCase()
			}
			return a
		}
		function A(b, c) {
			for (var d = g.greedy ? c : c.slice(0, 1), e = !1, f = 0; f < b.length; f++)
				if (a.inArray(b[f], d) !== -1) {
					e = !0;
					break
				}
			return e
		}
		function B(c, d, e, f, h) {
			function i(a) {
				return ia ? a.begin - a.end > 1 || a.begin - a.end === 1 && g.insertMode : a.end - a.begin > 1 || a.end - a.begin === 1 && g.insertMode
			}
			function j(b, d, e) {
				var h = !1;
				return a.each(v(b), function(j, k) {
					for (var l = k.match, q = d ? 1 : 0, r = "", t = l.cardinality; t > q; t--)
						r += F(b - (t - 1));
					if (d && (r += d), x(!0), h = null != l.fn ? l.fn.test(r, m(), b, e, g, i(c)) : (d === l.def || d === g.skipOptionalPartCharacter) && "" !== l.def && {
						c: l.placeholder || l.def,
						pos: b
					}, h !== !1) {
						var u = void 0 !== h.c ? h.c : d;
						u = u === g.skipOptionalPartCharacter && null === l.fn ? l.placeholder || l.def : u;
						var v = b,
							w = x();
						if (void 0 !== h.remove && (a.isArray(h.remove) || (h.remove = [h.remove]), a.each(h.remove.sort(function(a, b) {
							return b - a
						}), function(a, b) {
							p(b, b + 1, !0)
						})), void 0 !== h.insert && (a.isArray(h.insert) || (h.insert = [h.insert]), a.each(h.insert.sort(function(a, b) {
							return a - b
						}), function(a, b) {
							B(b.pos, b.c, !1, f)
						})), h.refreshFromBuffer) {
							var A = h.refreshFromBuffer;
							if (e = !0, y(A === !0 ? A : A.start, A.end, w), void 0 === h.pos && void 0 === h.c)
								return h.pos = o(), !1;
							if (v = void 0 !== h.pos ? h.pos : b, v !== b)
								return h = a.extend(h, B(v, u, !0, f)), !1
						} else if (h !== !0 && void 0 !== h.pos && h.pos !== b && (v = h.pos, y(b, v, x().slice()), v !== b))
							return h = a.extend(h, B(v, u, !0)), !1;
						return (h === !0 || void 0 !== h.pos || void 0 !== h.c) && (j > 0 && n(!0), s(v, a.extend({}, k, {
								input: z(u, l, v)
							}), f, i(c)) || (h = !1), !1)
					}
				}), h
			}
			function k(b, c, d) {
				var e,
					h,
					i,
					j,
					k,
					l,
					p,
					q,
					r = a.extend(!0, {}, m().validPositions),
					s = !1,
					t = o();
				for (j = m().validPositions[t]; t >= 0; t--)
					if (i = m().validPositions[t], i && void 0 !== i.alternation) {
						if (e = t, h = m().validPositions[e].alternation, j.locator[i.alternation] !== i.locator[i.alternation])
							break;
						j = i
					}
				if (void 0 !== h) {
					q = parseInt(e);
					var u = void 0 !== j.locator[j.alternation || h] ? j.locator[j.alternation || h] : p[0];
					u.length > 0 && (u = u.split(",")[0]);
					var w = m().validPositions[q],
						x = m().validPositions[q - 1];
					a.each(v(q, x ? x.locator : void 0, q - 1), function(e, i) {
						p = i.locator[h] ? i.locator[h].toString().split(",") : [];
						for (var j = 0; j < p.length; j++) {
							var t = [],
								v = 0,
								x = 0,
								y = !1;
							if (u < p[j] && (void 0 === i.na || a.inArray(p[j], i.na.split(",")) === -1)) {
								m().validPositions[q] = a.extend(!0, {}, i);
								var z = m().validPositions[q].locator;
								for (m().validPositions[q].locator[h] = parseInt(p[j]), null == i.match.fn ? (w.input !== i.match.def && (y = !0, w.generatedInput !== !0 && t.push(w.input)), x++, m().validPositions[q].generatedInput = !/[0-9a-bA-Z]/.test(i.match.def), m().validPositions[q].input = i.match.def) : m().validPositions[q].input = w.input, k = q + 1; k < o(void 0, !0) + 1; k++)
									l = m().validPositions[k],
									l && l.generatedInput !== !0 && /[0-9a-bA-Z]/.test(l.input) ? t.push(l.input) : k < b && v++,
									delete m().validPositions[k];
								for (y && t[0] === i.match.def && t.shift(), n(!0), s = !0; t.length > 0;) {
									var A = t.shift();
									if (A !== g.skipOptionalPartCharacter && !(s = B(o(void 0, !0) + 1, A, !1, f, !0)))
										break
								}
								if (s) {
									m().validPositions[q].locator = z;
									var C = o(b) + 1;
									for (k = q + 1; k < o() + 1; k++)
										l = m().validPositions[k],
										(void 0 === l || null == l.match.fn) && k < b + (x - v) && x++;
									b += x - v,
									s = B(b > C ? C : b, c, d, f, !0)
								}
								if (s)
									return !1;
								n(),
								m().validPositions = a.extend(!0, {}, r)
							}
						}
					})
				}
				return s
			}
			function l(b, c) {
				for (var d = m().validPositions[c], e = d.locator, f = e.length, g = b; g < c; g++)
					if (void 0 === m().validPositions[g] && !C(g, !0)) {
						var h = v(g),
							i = h[0],
							j = -1;
						a.each(h, function(a, b) {
							for (var c = 0; c < f && (void 0 !== b.locator[c] && A(b.locator[c].toString().split(","), e[c].toString().split(","))); c++)
								j < c && (j = c, i = b)
						}),
						s(g, a.extend({}, i, {
							input: i.match.placeholder || i.match.def
						}), !0)
					}
			}
			function s(b, c, d, e) {
				if (e || g.insertMode && void 0 !== m().validPositions[b] && void 0 === d) {
					var f,
						h = a.extend(!0, {}, m().validPositions),
						i = o();
					for (f = b; f <= i; f++)
						delete m().validPositions[f];
					m().validPositions[b] = a.extend(!0, {}, c);
					var j,
						k = !0,
						l = m().validPositions,
						p = !1,
						q = m().maskLength;
					for (f = j = b; f <= i; f++) {
						var r = h[f];
						if (void 0 !== r)
							for (var s = j; s < m().maskLength && (null == r.match.fn && l[f] && (l[f].match.optionalQuantifier === !0 || l[f].match.optionality === !0) || null != r.match.fn);) {
								if (s++, p === !1 && h[s] && h[s].match.def === r.match.def)
									m().validPositions[s] = a.extend(!0, {}, h[s]),
									m().validPositions[s].input = r.input,
									u(s),
									j = s,
									k = !0;
								else if (t(s, r.match.def)) {
									var v = B(s, r.input, !0, !0);
									k = v !== !1,
									j = v.caret || v.insert ? o() : s,
									p = !0
								} else
									k = r.generatedInput === !0;
								if (m().maskLength < q && (m().maskLength = q), k)
									break
							}
						if (!k)
							break
					}
					if (!k)
						return m().validPositions = a.extend(!0, {}, h), n(!0), !1
				} else
					m().validPositions[b] = a.extend(!0, {}, c);
				return n(!0), !0
			}
			function u(b) {
				for (var c = b - 1; c > -1 && !m().validPositions[c]; c--)
					;
				var d,
					e;
				for (c++; c < b; c++)
					void 0 === m().validPositions[c] && (g.jitMasking === !1 || g.jitMasking > c) && (e = v(c, r(c - 1).locator, c - 1).slice(), "" === e[e.length - 1].match.def && e.pop(), d = q(e), d && (d.match.def === g.radixPointDefinitionSymbol || !C(c, !0) || a.inArray(g.radixPoint, x()) < c && d.match.fn && d.match.fn.test(H(c), m(), c, !1, g)) && (E = j(c, d.match.placeholder || (null == d.match.fn ? d.match.def : "" !== H(c) ? H(c) : x()[c]), !0), E !== !1 && (m().validPositions[E.pos || c].generatedInput = !0)))
			}
			e = e === !0;
			var w = c;
			void 0 !== c.begin && (w = ia && !i(c) ? c.end : c.begin);
			var E = !1,
				G = a.extend(!0, {}, m().validPositions);
			if (u(w), i(c) && (P(void 0, b.keyCode.DELETE, c), w = m().p), w < m().maskLength && (E = j(w, d, e), (!e || f === !0) && E === !1)) {
				var I = m().validPositions[w];
				if (!I || null !== I.match.fn || I.match.def !== d && d !== g.skipOptionalPartCharacter) {
					if ((g.insertMode || void 0 === m().validPositions[D(w)]) && !C(w, !0)) {
						var J = v(w).slice();
						"" === J[J.length - 1].match.def && J.pop();
						var K = q(J, !0);
						K && (K = K.match.placeholder || K.match.def, j(w, K, e), m().validPositions[w].generatedInput = !0);
						for (var L = w + 1, M = D(w); L <= M; L++)
							if (E = j(L, d, e), E !== !1) {
								l(w, L),
								w = L;
								break
							}
					}
				} else
					E = {
						caret: D(w)
					}
			}
			return E === !1 && g.keepStatic && !e && h !== !0 && (E = k(w, d, e)), E === !0 && (E = {
				pos: w
			}), a.isFunction(g.postValidation) && E !== !1 && !e && f !== !0 && (E = !!g.postValidation(x(!0), E, g) && E), void 0 === E.pos && (E.pos = w), E === !1 && (n(!0), m().validPositions = a.extend(!0, {}, G)), E
		}
		function C(a, b) {
			var c;
			if (b ? (c = r(a).match, "" === c.def && (c = s(a).match)) : c = s(a).match, null != c.fn)
				return c.fn;
			if (b !== !0 && a > -1) {
				var d = v(a);
				return d.length > 1 + ("" === d[d.length - 1].match.def ? 1 : 0)
			}
			return !1
		}
		function D(a, b) {
			var c = m().maskLength;
			if (a >= c)
				return c;
			for (var d = a; ++d < c && (b === !0 && (s(d).match.newBlockMarker !== !0 || !C(d)) || b !== !0 && !C(d));)
				;
			return d
		}
		function E(a, b) {
			var c,
				d = a;
			if (d <= 0)
				return 0;
			for (; --d > 0 && (b === !0 && s(d).match.newBlockMarker !== !0 || b !== !0 && !C(d) && (c = v(d), c.length < 2 || 2 === c.length && "" === c[1].match.def));)
				;
			return d
		}
		function F(a) {
			return void 0 === m().validPositions[a] ? H(a) : m().validPositions[a].input
		}
		function G(b, c, d, e, f) {
			if (e && a.isFunction(g.onBeforeWrite)) {
				var h = g.onBeforeWrite(e, c, d, g);
				if (h) {
					if (h.refreshFromBuffer) {
						var i = h.refreshFromBuffer;
						y(i === !0 ? i : i.start, i.end, h.buffer || c),
						c = x(!0)
					}
					void 0 !== d && (d = void 0 !== h.caret ? h.caret : d)
				}
			}
			b.inputmask._valueSet(c.join("")),
			void 0 === d || void 0 !== e && "blur" === e.type || K(b, d),
			f === !0 && (ka = !0, a(b).trigger("input"))
		}
		function H(a, b) {
			if (b = b || s(a).match, void 0 !== b.placeholder)
				return b.placeholder;
			if (null === b.fn) {
				if (a > -1 && void 0 === m().validPositions[a]) {
					var c,
						d = v(a),
						e = [];
					if (d.length > 1 + ("" === d[d.length - 1].match.def ? 1 : 0))
						for (var f = 0; f < d.length; f++)
							if (d[f].match.optionality !== !0 && d[f].match.optionalQuantifier !== !0 && (null === d[f].match.fn || void 0 === c || d[f].match.fn.test(c.match.def, m(), a, !0, g) !== !1) && (e.push(d[f]), null === d[f].match.fn && (c = d[f]), e.length > 1 && /[0-9a-bA-Z]/.test(e[0].match.def)))
								return g.placeholder.charAt(a % g.placeholder.length)
				}
				return b.def
			}
			return g.placeholder.charAt(a % g.placeholder.length)
		}
		function I(c, d, e, f, h, i) {
			function j() {
				var a = !1,
					b = w().slice(p, D(p)).join("").indexOf(l);
				if (b !== -1 && !C(p)) {
					a = !0;
					for (var c = w().slice(p, p + b), d = 0; d < c.length; d++)
						if (" " !== c[d]) {
							a = !1;
							break
						}
				}
				return a
			}
			var k = f.slice(),
				l = "",
				p = 0,
				q = void 0;
			if (n(), m().p = D(-1), !e)
				if (g.autoUnmask !== !0) {
					var s = w().slice(0, D(-1)).join(""),
						t = k.join("").match(new RegExp("^" + b.escapeRegex(s), "g"));
					t && t.length > 0 && (k.splice(0, t.length * s.length), p = D(p))
				} else
					p = D(p);
			if (a.each(k, function(b, d) {
				if (void 0 !== d) {
					var f = new a.Event("keypress");
					f.which = d.charCodeAt(0),
					l += d;
					var h = o(void 0, !0),
						i = m().validPositions[h],
						k = r(h + 1, i ? i.locator.slice() : void 0, h);
					if (!j() || e || g.autoUnmask) {
						var s = e ? b : null == k.match.fn && k.match.optionality && h + 1 < m().p ? h + 1 : m().p;
						q = R.call(c, f, !0, !1, e, s),
						p = s + 1,
						l = ""
					} else
						q = R.call(c, f, !0, !1, !0, h + 1);
					if (!e && a.isFunction(g.onBeforeWrite) && (q = g.onBeforeWrite(f, x(), q.forwardPosition, g), q && q.refreshFromBuffer)) {
						var t = q.refreshFromBuffer;
						y(t === !0 ? t : t.start, t.end, q.buffer),
						n(!0),
						q.caret && (m().p = q.caret)
					}
				}
			}), d) {
				var u = void 0,
					v = o();
				document.activeElement === c && (h || q) && (u = K(c).begin, h && q === !1 && (u = D(o(u))), q && i !== !0 && (u < v + 1 || v === -1) && (u = g.numericInput && void 0 === q.caret ? E(q.forwardPosition) : q.forwardPosition)),
				G(c, x(), u, h || new a.Event("checkval"))
			}
		}
		function J(b) {
			if (b && void 0 === b.inputmask)
				return b.value;
			var c = [],
				d = m().validPositions;
			for (var e in d)
				d[e].match && null != d[e].match.fn && c.push(d[e].input);
			var f = 0 === c.length ? "" : (ia ? c.reverse() : c).join("");
			if (a.isFunction(g.onUnMask)) {
				var h = (ia ? x().slice().reverse() : x()).join("");
				f = g.onUnMask(h, f, g) || f
			}
			return f
		}
		function K(a, b, c, d) {
			function e(a) {
				if (d !== !0 && ia && "number" == typeof a && (!g.greedy || "" !== g.placeholder)) {
					var b = x().join("").length;
					a = b - a
				}
				return a
			}
			var f;
			if ("number" != typeof b)
				return a.setSelectionRange ? (b = a.selectionStart, c = a.selectionEnd) : window.getSelection ? (f = window.getSelection().getRangeAt(0), f.commonAncestorContainer.parentNode !== a && f.commonAncestorContainer !== a || (b = f.startOffset, c = f.endOffset)) : document.selection && document.selection.createRange && (f = document.selection.createRange(), b = 0 - f.duplicate().moveStart("character", -a.inputmask._valueGet().length), c = b + f.text.length), {
					begin: e(b),
					end: e(c)
				};
			b = e(b),
			c = e(c),
			c = "number" == typeof c ? c : b;
			var h = parseInt(((a.ownerDocument.defaultView || window).getComputedStyle ? (a.ownerDocument.defaultView || window).getComputedStyle(a, null) : a.currentStyle).fontSize) * c;
			if (a.scrollLeft = h > a.scrollWidth ? h : 0, j || g.insertMode !== !1 || b !== c || c++, a.setSelectionRange)
				a.selectionStart = b,
				a.selectionEnd = c;
			else if (window.getSelection) {
				if (f = document.createRange(), void 0 === a.firstChild || null === a.firstChild) {
					var i = document.createTextNode("");
					a.appendChild(i)
				}
				f.setStart(a.firstChild, b < a.inputmask._valueGet().length ? b : a.inputmask._valueGet().length),
				f.setEnd(a.firstChild, c < a.inputmask._valueGet().length ? c : a.inputmask._valueGet().length),
				f.collapse(!0);
				var k = window.getSelection();
				k.removeAllRanges(),
				k.addRange(f)
			} else
				a.createTextRange && (f = a.createTextRange(), f.collapse(!0), f.moveEnd("character", c), f.moveStart("character", b), f.select())
		}
		function L(b) {
			var c,
				d,
				e = x(),
				f = e.length,
				g = o(),
				h = {},
				i = m().validPositions[g],
				j = void 0 !== i ? i.locator.slice() : void 0;
			for (c = g + 1; c < e.length; c++)
				d = r(c, j, c - 1),
				j = d.locator.slice(),
				h[c] = a.extend(!0, {}, d);
			var k = i && void 0 !== i.alternation ? i.locator[i.alternation] : void 0;
			for (c = f - 1; c > g && (d = h[c], (d.match.optionality || d.match.optionalQuantifier || k && (k !== h[c].locator[i.alternation] && null != d.match.fn || null === d.match.fn && d.locator[i.alternation] && A(d.locator[i.alternation].toString().split(","), k.toString().split(",")) && "" !== v(c)[0].def)) && e[c] === H(c, d.match)); c--)
				f--;
			return b ? {
				l: f,
				def: h[f] ? h[f].match : void 0
			} : f
		}
		function M(a) {
			for (var b = L(), c = a.length - 1; c > b && !C(c); c--)
				;
			return a.splice(b, c + 1 - b), a
		}
		function N(b) {
			if (a.isFunction(g.isComplete))
				return g.isComplete(b, g);
			if ("*" !== g.repeat) {
				var c = !1,
					d = L(!0),
					e = E(d.l);
				if (void 0 === d.def || d.def.newBlockMarker || d.def.optionality || d.def.optionalQuantifier) {
					c = !0;
					for (var f = 0; f <= e; f++) {
						var h = r(f).match;
						if (null !== h.fn && void 0 === m().validPositions[f] && h.optionality !== !0 && h.optionalQuantifier !== !0 || null === h.fn && b[f] !== H(f, h)) {
							c = !1;
							break
						}
					}
				}
				return c
			}
		}
		function O(b) {
			function c(b) {
				if (a.valHooks && (void 0 === a.valHooks[b] || a.valHooks[b].inputmaskpatch !== !0)) {
					var c = a.valHooks[b] && a.valHooks[b].get ? a.valHooks[b].get : function(a) {
							return a.value
						},
						d = a.valHooks[b] && a.valHooks[b].set ? a.valHooks[b].set : function(a, b) {
							return a.value = b, a
						};
					a.valHooks[b] = {
						get: function(a) {
							if (a.inputmask) {
								if (a.inputmask.opts.autoUnmask)
									return a.inputmask.unmaskedvalue();
								var b = c(a);
								return o(void 0, void 0, a.inputmask.maskset.validPositions) !== -1 || g.nullable !== !0 ? b : ""
							}
							return c(a)
						},
						set: function(b, c) {
							var e,
								f = a(b);
							return e = d(b, c), b.inputmask && f.trigger("setvalue"), e
						},
						inputmaskpatch: !0
					}
				}
			}
			function d() {
				return this.inputmask ? this.inputmask.opts.autoUnmask ? this.inputmask.unmaskedvalue() : o() !== -1 || g.nullable !== !0 ? document.activeElement === this && g.clearMaskOnLostFocus ? (ia ? M(x().slice()).reverse() : M(x().slice())).join("") : h.call(this) : "" : h.call(this)
			}
			function e(b) {
				i.call(this, b),
				this.inputmask && a(this).trigger("setvalue")
			}
			function f(b) {
				oa.on(b, "mouseenter", function(b) {
					var c = a(this),
						d = this,
						e = d.inputmask._valueGet();
					e !== x().join("") && c.trigger("setvalue")
				})
			}
			var h,
				i;
			if (!b.inputmask.__valueGet) {
				if (g.noValuePatching !== !0) {
					if (Object.getOwnPropertyDescriptor) {
						"function" != typeof Object.getPrototypeOf && (Object.getPrototypeOf = "object" == typeof "test".__proto__ ? function(a) {
							return a.__proto__
						} : function(a) {
							return a.constructor.prototype
						});
						var j = Object.getPrototypeOf ? Object.getOwnPropertyDescriptor(Object.getPrototypeOf(b), "value") : void 0;
						j && j.get && j.set ? (h = j.get, i = j.set, Object.defineProperty(b, "value", {
							get: d,
							set: e,
							configurable: !0
						})) : "INPUT" !== b.tagName && (h = function() {
							return this.textContent
						}, i = function(a) {
							this.textContent = a
						}, Object.defineProperty(b, "value", {
							get: d,
							set: e,
							configurable: !0
						}))
					} else
						document.__lookupGetter__ && b.__lookupGetter__("value") && (h = b.__lookupGetter__("value"), i = b.__lookupSetter__("value"), b.__defineGetter__("value", d), b.__defineSetter__("value", e));
					b.inputmask.__valueGet = h,
					b.inputmask.__valueSet = i
				}
				b.inputmask._valueGet = function(a) {
					return ia && a !== !0 ? h.call(this.el).split("").reverse().join("") : h.call(this.el)
				},
				b.inputmask._valueSet = function(a, b) {
					i.call(this.el, null === a || void 0 === a ? "" : b !== !0 && ia ? a.split("").reverse().join("") : a)
				},
				void 0 === h && (h = function() {
					return this.value
				}, i = function(a) {
					this.value = a
				}, c(b.type), f(b))
			}
		}
		function P(c, d, e, f) {
			function h() {
				if (g.keepStatic) {
					for (var b = [], d = o(-1, !0), e = a.extend(!0, {}, m().validPositions), f = m().validPositions[d]; d >= 0; d--) {
						var h = m().validPositions[d];
						if (h) {
							if (h.generatedInput !== !0 && /[0-9a-bA-Z]/.test(h.input) && b.push(h.input), delete m().validPositions[d], void 0 !== h.alternation && h.locator[h.alternation] !== f.locator[h.alternation])
								break;
							f = h
						}
					}
					if (d > -1)
						for (m().p = D(o(-1, !0)); b.length > 0;) {
							var i = new a.Event("keypress");
							i.which = b.pop().charCodeAt(0),
							R.call(c, i, !0, !1, !1, m().p)
						}
					else
						m().validPositions = a.extend(!0, {}, e)
				}
			}
			if ((g.numericInput || ia) && (d === b.keyCode.BACKSPACE ? d = b.keyCode.DELETE : d === b.keyCode.DELETE && (d = b.keyCode.BACKSPACE), ia)) {
				var i = e.end;
				e.end = e.begin,
				e.begin = i
			}
			d === b.keyCode.BACKSPACE && (e.end - e.begin < 1 || g.insertMode === !1) ? (e.begin = E(e.begin), void 0 === m().validPositions[e.begin] || m().validPositions[e.begin].input !== g.groupSeparator && m().validPositions[e.begin].input !== g.radixPoint || e.begin--) : d === b.keyCode.DELETE && e.begin === e.end && (e.end = C(e.end, !0) ? e.end + 1 : D(e.end) + 1, void 0 === m().validPositions[e.begin] || m().validPositions[e.begin].input !== g.groupSeparator && m().validPositions[e.begin].input !== g.radixPoint || e.end++),
			p(e.begin, e.end, !1, f),
			f !== !0 && h();
			var j = o(e.begin, !0);
			j < e.begin ? m().p = D(j) : f !== !0 && (m().p = e.begin)
		}
		function Q(d) {
			var e = this,
				f = a(e),
				h = d.keyCode,
				i = K(e);
			if (h === b.keyCode.BACKSPACE || h === b.keyCode.DELETE || l && h === b.keyCode.BACKSPACE_SAFARI || d.ctrlKey && h === b.keyCode.X && !c("cut"))
				d.preventDefault(),
				P(e, h, i),
				G(e, x(!0), m().p, d, e.inputmask._valueGet() !== x().join("")),
				e.inputmask._valueGet() === w().join("") ? f.trigger("cleared") : N(x()) === !0 && f.trigger("complete"),
				g.showTooltip && (e.title = g.tooltip || m().mask);
			else if (h === b.keyCode.END || h === b.keyCode.PAGE_DOWN) {
				d.preventDefault();
				var j = D(o());
				g.insertMode || j !== m().maskLength || d.shiftKey || j--,
				K(e, d.shiftKey ? i.begin : j, j, !0)
			} else
				h === b.keyCode.HOME && !d.shiftKey || h === b.keyCode.PAGE_UP ? (d.preventDefault(), K(e, 0, d.shiftKey ? i.begin : 0, !0)) : (g.undoOnEscape && h === b.keyCode.ESCAPE || 90 === h && d.ctrlKey) && d.altKey !== !0 ? (I(e, !0, !1, da.split("")), f.trigger("click")) : h !== b.keyCode.INSERT || d.shiftKey || d.ctrlKey ? g.tabThrough === !0 && h === b.keyCode.TAB ? (d.shiftKey === !0 ? (null === s(i.begin).match.fn && (i.begin = D(i.begin)), i.end = E(i.begin, !0), i.begin = E(i.end, !0)) : (i.begin = D(i.begin, !0), i.end = D(i.begin, !0), i.end < m().maskLength && i.end--), i.begin < m().maskLength && (d.preventDefault(), K(e, i.begin, i.end))) : g.insertMode !== !1 || d.shiftKey || (h === b.keyCode.RIGHT ? setTimeout(function() {
					var a = K(e);
					K(e, a.begin)
				}, 0) : h === b.keyCode.LEFT && setTimeout(function() {
					var a = K(e);
					K(e, ia ? a.begin + 1 : a.begin - 1)
				}, 0)) : (g.insertMode = !g.insertMode, K(e, g.insertMode || i.begin !== m().maskLength ? i.begin : i.begin - 1));
			g.onKeyDown.call(this, d, x(), K(e).begin, g),
			ma = a.inArray(h, g.ignorables) !== -1
		}
		function R(c, d, e, f, h) {
			var i = this,
				j = a(i),
				k = c.which || c.charCode || c.keyCode;
			if (!(d === !0 || c.ctrlKey && c.altKey) && (c.ctrlKey || c.metaKey || ma))
				return k === b.keyCode.ENTER && da !== x().join("") && (da = x().join(""), setTimeout(function() {
					j.trigger("change")
				}, 0)), !0;
			if (k) {
				46 === k && c.shiftKey === !1 && "," === g.radixPoint && (k = 44);
				var l,
					o = d ? {
						begin: h,
						end: h
					} : K(i),
					p = String.fromCharCode(k);
				m().writeOutBuffer = !0;
				var q = B(o, p, f);
				if (q !== !1 && (n(!0), l = void 0 !== q.caret ? q.caret : d ? q.pos + 1 : D(q.pos), m().p = l), e !== !1) {
					var r = this;
					if (setTimeout(function() {
						g.onKeyValidation.call(r, k, q, g)
					}, 0), m().writeOutBuffer && q !== !1) {
						var s = x();
						G(i, s, g.numericInput && void 0 === q.caret ? E(l) : l, c, d !== !0),
						d !== !0 && setTimeout(function() {
							N(s) === !0 && j.trigger("complete")
						}, 0)
					}
				}
				if (g.showTooltip && (i.title = g.tooltip || m().mask), c.preventDefault(), d)
					return q.forwardPosition = l, q
			}
		}
		function S(b) {
			var c,
				d = this,
				e = b.originalEvent || b,
				f = a(d),
				h = d.inputmask._valueGet(!0),
				i = K(d);
			ia && (c = i.end, i.end = i.begin, i.begin = c);
			var j = h.substr(0, i.begin),
				k = h.substr(i.end, h.length);
			if (j === (ia ? w().reverse() : w()).slice(0, i.begin).join("") && (j = ""), k === (ia ? w().reverse() : w()).slice(i.end).join("") && (k = ""), ia && (c = j, j = k, k = c), window.clipboardData && window.clipboardData.getData)
				h = j + window.clipboardData.getData("Text") + k;
			else {
				if (!e.clipboardData || !e.clipboardData.getData)
					return !0;
				h = j + e.clipboardData.getData("text/plain") + k
			}
			var l = h;
			if (a.isFunction(g.onBeforePaste)) {
				if (l = g.onBeforePaste(h, g), l === !1)
					return b.preventDefault();
				l || (l = h)
			}
			return I(d, !1, !1, ia ? l.split("").reverse() : l.toString().split("")), G(d, x(), D(o()), b, da !== x().join("")), N(x()) === !0 && f.trigger("complete"), b.preventDefault()
		}
		function T(c) {
			var d = this,
				e = d.inputmask._valueGet();
			if (x().join("") !== e) {
				var f = K(d);
				if (e = e.replace(new RegExp("(" + b.escapeRegex(w().join("")) + ")*"), ""), k) {
					var g = e.replace(x().join(""), "");
					if (1 === g.length) {
						var h = new a.Event("keypress");
						return h.which = g.charCodeAt(0), R.call(d, h, !0, !0, !1, m().validPositions[f.begin - 1] ? f.begin : f.begin - 1), !1
					}
				}
				if (f.begin > e.length && (K(d, e.length), f = K(d)), x().length - e.length !== 1 || e.charAt(f.begin) === x()[f.begin] || e.charAt(f.begin + 1) === x()[f.begin] || C(f.begin)) {
					for (var i = o() + 1, j = x().slice(i).join(""); null === e.match(b.escapeRegex(j) + "$");)
						j = j.slice(1);
					e = e.replace(j, ""),
					e = e.split(""),
					I(d, !0, !1, e, c, f.begin < i),
					N(x()) === !0 && a(d).trigger("complete")
				} else
					c.keyCode = b.keyCode.BACKSPACE,
					Q.call(d, c);
				c.preventDefault()
			}
		}
		function U(b) {
			var c = this,
				d = c.inputmask._valueGet();
			I(c, !0, !1, (a.isFunction(g.onBeforeMask) ? g.onBeforeMask(d, g) || d : d).split("")),
			da = x().join(""),
			(g.clearMaskOnLostFocus || g.clearIncomplete) && c.inputmask._valueGet() === w().join("") && c.inputmask._valueSet("")
		}
		function V(a) {
			var b = this,
				c = b.inputmask._valueGet();
			g.showMaskOnFocus && (!g.showMaskOnHover || g.showMaskOnHover && "" === c) ? b.inputmask._valueGet() !== x().join("") && G(b, x(), D(o())) : na === !1 && K(b, D(o())),
			g.positionCaretOnTab === !0 && setTimeout(function() {
				X.apply(this, [a])
			}, 0),
			da = x().join("")
		}
		function W(a) {
			var b = this;
			if (na = !1, g.clearMaskOnLostFocus && document.activeElement !== b) {
				var c = x().slice(),
					d = b.inputmask._valueGet();
				d !== b.getAttribute("placeholder") && "" !== d && (o() === -1 && d === w().join("") ? c = [] : M(c), G(b, c))
			}
		}
		function X(b) {
			function c(b) {
				if ("" !== g.radixPoint) {
					var c = m().validPositions;
					if (void 0 === c[b] || c[b].input === H(b)) {
						if (b < D(-1))
							return !0;
						var d = a.inArray(g.radixPoint, x());
						if (d !== -1) {
							for (var e in c)
								if (d < e && c[e].input !== H(e))
									return !1;
							return !0
						}
					}
				}
				return !1
			}
			var d = this;
			setTimeout(function() {
				if (document.activeElement === d) {
					var b = K(d);
					if (b.begin === b.end)
						switch (g.positionCaretOnClick) {
						case "none":
							break;
						case "radixFocus":
							if (c(b.begin)) {
								var e = a.inArray(g.radixPoint, x().join(""));
								K(d, g.numericInput ? D(e) : e);
								break
							}
						default:
							var f = b.begin,
								h = o(f, !0),
								i = D(h);
							if (f < i)
								K(d, C(f) || C(f - 1) ? f : D(f));
							else {
								var j = H(i);
								("" !== j && x()[i] !== j && s(i).match.optionalQuantifier !== !0 || !C(i, !0) && s(i).match.def === j) && (i = D(i)),
								K(d, i)
							}
						}
				}
			}, 0)
		}
		function Y(a) {
			var b = this;
			setTimeout(function() {
				K(b, 0, D(o()))
			}, 0)
		}
		function Z(c) {
			var d = this,
				e = a(d),
				f = K(d),
				h = c.originalEvent || c,
				i = window.clipboardData || h.clipboardData,
				j = ia ? x().slice(f.end, f.begin) : x().slice(f.begin, f.end);
			i.setData("text", ia ? j.reverse().join("") : j.join("")),
			document.execCommand && document.execCommand("copy"),
			P(d, b.keyCode.DELETE, f),
			G(d, x(), m().p, c, da !== x().join("")),
			d.inputmask._valueGet() === w().join("") && e.trigger("cleared"),
			g.showTooltip && (d.title = g.tooltip || m().mask)
		}
		function $(b) {
			var c = a(this),
				d = this;
			if (d.inputmask) {
				var e = d.inputmask._valueGet(),
					f = x().slice();
				da !== f.join("") && setTimeout(function() {
					c.trigger("change"),
					da = f.join("")
				}, 0),
				"" !== e && (g.clearMaskOnLostFocus && (o() === -1 && e === w().join("") ? f = [] : M(f)), N(f) === !1 && (setTimeout(function() {
					c.trigger("incomplete")
				}, 0), g.clearIncomplete && (n(), f = g.clearMaskOnLostFocus ? [] : w().slice())), G(d, f, void 0, b))
			}
		}
		function _(a) {
			var b = this;
			na = !0,
			document.activeElement !== b && g.showMaskOnHover && b.inputmask._valueGet() !== x().join("") && G(b, x())
		}
		function aa(a) {
			da !== x().join("") && fa.trigger("change"),
			g.clearMaskOnLostFocus && o() === -1 && ea.inputmask._valueGet && ea.inputmask._valueGet() === w().join("") && ea.inputmask._valueSet(""),
			g.removeMaskOnSubmit && (ea.inputmask._valueSet(ea.inputmask.unmaskedvalue(), !0), setTimeout(function() {
				G(ea, x())
			}, 0))
		}
		function ba(a) {
			setTimeout(function() {
				fa.trigger("setvalue")
			}, 0)
		}
		function ca(b) {
			if (ea = b, fa = a(ea), g.showTooltip && (ea.title = g.tooltip || m().mask), ("rtl" === ea.dir || g.rightAlign) && (ea.style.textAlign = "right"), ("rtl" === ea.dir || g.numericInput) && (ea.dir = "ltr", ea.removeAttribute("dir"), ea.inputmask.isRTL = !0, ia = !0), j && (ea.setAttribute("inputmode", "verbatim"), ea.setAttribute("x-inputmode", "verbatim")), oa.off(ea), O(ea), d(ea, g) && (oa.on(ea, "submit", aa), oa.on(ea, "reset", ba), oa.on(ea, "mouseenter", _), oa.on(ea, "blur", $), oa.on(ea, "focus", V), oa.on(ea, "mouseleave", W), oa.on(ea, "click", X), oa.on(ea, "dblclick", Y), oa.on(ea, "paste", S), oa.on(ea, "dragdrop", S), oa.on(ea, "drop", S), oa.on(ea, "cut", Z), oa.on(ea, "complete", g.oncomplete), oa.on(ea, "incomplete", g.onincomplete), oa.on(ea, "cleared", g.oncleared), g.inputEventOnly !== !0 && (oa.on(ea, "keydown", Q), oa.on(ea, "keypress", R)), oa.on(ea, "compositionstart", a.noop), oa.on(ea, "compositionend", a.noop), oa.on(ea, "input", T)), oa.on(ea, "setvalue", U), w(), "" !== ea.inputmask._valueGet() || g.clearMaskOnLostFocus === !1 || document.activeElement === ea) {
				var c = a.isFunction(g.onBeforeMask) ? g.onBeforeMask(ea.inputmask._valueGet(), g) || ea.inputmask._valueGet() : ea.inputmask._valueGet();
				I(ea, !0, !1, c.split(""));
				var e = x().slice();
				da = e.join(""),
				N(e) === !1 && g.clearIncomplete && n(),
				g.clearMaskOnLostFocus && document.activeElement !== ea && (o() === -1 ? e = [] : M(e)),
				G(ea, e),
				document.activeElement === ea && K(ea, D(o()))
			}
		}
		var da,
			ea,
			fa,
			ga,
			ha,
			ia = !1,
			ja = !1,
			ka = !1,
			la = !1,
			ma = !1,
			na = !0,
			oa = {
				on: function(c, d, e) {
					var f = function(c) {
						if (void 0 === this.inputmask && "FORM" !== this.nodeName) {
							var d = a.data(this, "_inputmask_opts");
							d ? new b(d).mask(this) : oa.off(this)
						} else {
							if ("setvalue" === c.type || !(this.disabled || this.readOnly && !("keydown" === c.type && c.ctrlKey && 67 === c.keyCode || g.tabThrough === !1 && c.keyCode === b.keyCode.TAB))) {
								switch (c.type) {
								case "input":
									if (ka === !0)
										return ka = !1, c.preventDefault();
									break;
								case "keydown":
									ja = !1,
									ka = !1;
									break;
								case "keypress":
									if (ja === !0)
										return c.preventDefault();
									ja = !0;
									break;
								case "click":
									if (k || l) {
										var f = this,
											h = arguments;
										return setTimeout(function() {
											e.apply(f, h)
										}, 0), !1
									}
									break;
								case "compositionstart":
									la = !0;
									break;
								case "compositionend":
									la = !1
								}
								var i = e.apply(this, arguments);
								return i === !1 && (c.preventDefault(), c.stopPropagation()), i
							}
							c.preventDefault()
						}
					};
					c.inputmask.events[d] = c.inputmask.events[d] || [],
					c.inputmask.events[d].push(f),
					a.inArray(d, ["submit", "reset"]) !== -1 ? null != c.form && a(c.form).on(d, f) : a(c).on(d, f)
				},
				off: function(b, c) {
					if (b.inputmask && b.inputmask.events) {
						var d;
						c ? (d = [], d[c] = b.inputmask.events[c]) : d = b.inputmask.events,
						a.each(d, function(c, d) {
							for (; d.length > 0;) {
								var e = d.pop();
								a.inArray(c, ["submit", "reset"]) !== -1 ? null != b.form && a(b.form).off(c, e) : a(b).off(c, e)
							}
							delete b.inputmask.events[c]
						})
					}
				}
			};
		if (void 0 !== e)
			switch (e.action) {
			case "isComplete":
				return ea = e.el, N(x());
			case "unmaskedvalue":
				return ea = e.el, void 0 !== ea && void 0 !== ea.inputmask ? (f = ea.inputmask.maskset, g = ea.inputmask.opts, ia = ea.inputmask.isRTL) : (ha = e.value, g.numericInput && (ia = !0), ha = (a.isFunction(g.onBeforeMask) ? g.onBeforeMask(ha, g) || ha : ha).split(""), I(void 0, !1, !1, ia ? ha.reverse() : ha), a.isFunction(g.onBeforeWrite) && g.onBeforeWrite(void 0, x(), 0, g)), J(ea);
			case "mask":
				ea = e.el,
				f = ea.inputmask.maskset,
				g = ea.inputmask.opts,
				ia = ea.inputmask.isRTL,
				ca(ea);
				break;
			case "format":
				return g.numericInput && (ia = !0), ha = (a.isFunction(g.onBeforeMask) ? g.onBeforeMask(e.value, g) || e.value : e.value).split(""), I(void 0, !1, !1, ia ? ha.reverse() : ha), a.isFunction(g.onBeforeWrite) && g.onBeforeWrite(void 0, x(), 0, g), e.metadata ? {
					value: ia ? x().slice().reverse().join("") : x().join(""),
					metadata: h({
						action: "getmetadata"
					}, f, g)
				} : ia ? x().slice().reverse().join("") : x().join("");
			case "isValid":
				g.numericInput && (ia = !0),
				e.value ? (ha = e.value.split(""), I(void 0, !1, !0, ia ? ha.reverse() : ha)) : e.value = x().join("");
				for (var pa = x(), qa = L(), ra = pa.length - 1; ra > qa && !C(ra); ra--)
					;
				return pa.splice(qa, ra + 1 - qa), N(pa) && e.value === x().join("");
			case "getemptymask":
				return w().join("");
			case "remove":
				ea = e.el,
				fa = a(ea),
				f = ea.inputmask.maskset,
				g = ea.inputmask.opts,
				ea.inputmask._valueSet(J(ea)),
				oa.off(ea);
				var sa;
				Object.getOwnPropertyDescriptor && Object.getPrototypeOf ? (sa = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(ea), "value"), sa && ea.inputmask.__valueGet && Object.defineProperty(ea, "value", {
					get: ea.inputmask.__valueGet,
					set: ea.inputmask.__valueSet,
					configurable: !0
				})) : document.__lookupGetter__ && ea.__lookupGetter__("value") && ea.inputmask.__valueGet && (ea.__defineGetter__("value", ea.inputmask.__valueGet), ea.__defineSetter__("value", ea.inputmask.__valueSet)),
				ea.inputmask = void 0;
				break;
			case "getmetadata":
				if (a.isArray(f.metadata)) {
					for (var ta, ua = o(void 0, !0), va = ua; va >= 0; va--)
						if (m().validPositions[va] && void 0 !== m().validPositions[va].alternation) {
							ta = m().validPositions[va].alternation;
							break
						}
					return void 0 !== ta ? f.metadata[m().validPositions[va].locator[ta]] : []
				}
				return f.metadata
			}
	}
	b.prototype = {
		defaults: {
			placeholder: "_",
			optionalmarker: {
				start: "[",
				end: "]"
			},
			quantifiermarker: {
				start: "{",
				end: "}"
			},
			groupmarker: {
				start: "(",
				end: ")"
			},
			alternatormarker: "|",
			escapeChar: "\\",
			mask: null,
			oncomplete: a.noop,
			onincomplete: a.noop,
			oncleared: a.noop,
			repeat: 0,
			greedy: !0,
			autoUnmask: !1,
			removeMaskOnSubmit: !1,
			clearMaskOnLostFocus: !0,
			insertMode: !0,
			clearIncomplete: !1,
			aliases: {},
			alias: null,
			onKeyDown: a.noop,
			onBeforeMask: null,
			onBeforePaste: function(b, c) {
				return a.isFunction(c.onBeforeMask) ? c.onBeforeMask(b, c) : b
			},
			onBeforeWrite: null,
			onUnMask: null,
			showMaskOnFocus: !0,
			showMaskOnHover: !0,
			onKeyValidation: a.noop,
			skipOptionalPartCharacter: " ",
			showTooltip: !1,
			tooltip: void 0,
			numericInput: !1,
			rightAlign: !1,
			undoOnEscape: !0,
			radixPoint: "",
			radixPointDefinitionSymbol: void 0,
			groupSeparator: "",
			keepStatic: null,
			positionCaretOnTab: !0,
			tabThrough: !1,
			supportsInputType: ["text", "tel", "password"],
			definitions: {
				9: {
					validator: "[0-9]",
					cardinality: 1,
					definitionSymbol: "*"
				},
				a: {
					validator: "[A-Za-z\u0410-\u044f\u0401\u0451\xc0-\xff\xb5]",
					cardinality: 1,
					definitionSymbol: "*"
				},
				"*": {
					validator: "[0-9A-Za-z\u0410-\u044f\u0401\u0451\xc0-\xff\xb5]",
					cardinality: 1
				}
			},
			ignorables: [8, 9, 13, 19, 27, 33, 34, 35, 36, 37, 38, 39, 40, 45, 46, 93, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123],
			isComplete: null,
			canClearPosition: a.noop,
			postValidation: null,
			staticDefinitionSymbol: void 0,
			jitMasking: !1,
			nullable: !0,
			inputEventOnly: !1,
			noValuePatching: !1,
			positionCaretOnClick: "lvp",
			casing: null
		},
		masksCache: {},
		mask: function(c) {
			var d = this;
			return "string" == typeof c && (c = document.getElementById(c) || document.querySelectorAll(c)), c = c.nodeName ? [c] : c, a.each(c, function(c, e) {
				var i = a.extend(!0, {}, d.opts);
				f(e, i, a.extend(!0, {}, d.userOptions));
				var j = g(i, d.noMasksCache);
				void 0 !== j && (void 0 !== e.inputmask && e.inputmask.remove(), e.inputmask = new b, e.inputmask.opts = i, e.inputmask.noMasksCache = d.noMasksCache, e.inputmask.userOptions = a.extend(!0, {}, d.userOptions), e.inputmask.el = e, e.inputmask.maskset = j, e.inputmask.isRTL = !1, a.data(e, "_inputmask_opts", i), h({
					action: "mask",
					el: e
				}))
			}), c && c[0] ? c[0].inputmask || this : this
		},
		option: function(b, c) {
			return "string" == typeof b ? this.opts[b] : "object" == typeof b ? (a.extend(this.userOptions, b), this.el && c !== !0 && this.mask(this.el), this) : void 0
		},
		unmaskedvalue: function(a) {
			return h({
				action: "unmaskedvalue",
				el: this.el,
				value: a
			}, this.el && this.el.inputmask ? this.el.inputmask.maskset : g(this.opts, this.noMasksCache), this.opts)
		},
		remove: function() {
			if (this.el)
				return h({
					action: "remove",
					el: this.el
				}), this.el.inputmask = void 0, this.el
		},
		getemptymask: function() {
			return h({
				action: "getemptymask"
			}, this.maskset || g(this.opts, this.noMasksCache), this.opts)
		},
		hasMaskedValue: function() {
			return !this.opts.autoUnmask
		},
		isComplete: function() {
			return h({
				action: "isComplete",
				el: this.el
			}, this.maskset || g(this.opts, this.noMasksCache), this.opts)
		},
		getmetadata: function() {
			return h({
				action: "getmetadata"
			}, this.maskset || g(this.opts, this.noMasksCache), this.opts)
		},
		isValid: function(a) {
			return h({
				action: "isValid",
				value: a
			}, this.maskset || g(this.opts, this.noMasksCache), this.opts)
		},
		format: function(a, b) {
			return h({
				action: "format",
				value: a,
				metadata: b
			}, this.maskset || g(this.opts, this.noMasksCache), this.opts)
		}
	},
	b.extendDefaults = function(c) {
		a.extend(!0, b.prototype.defaults, c)
	},
	b.extendDefinitions = function(c) {
		a.extend(!0, b.prototype.defaults.definitions, c)
	},
	b.extendAliases = function(c) {
		a.extend(!0, b.prototype.defaults.aliases, c)
	},
	b.format = function(a, c, d) {
		return b(c).format(a, d)
	},
	b.unmask = function(a, c) {
		return b(c).unmaskedvalue(a)
	},
	b.isValid = function(a, c) {
		return b(c).isValid(a)
	},
	b.remove = function(b) {
		a.each(b, function(a, b) {
			b.inputmask && b.inputmask.remove()
		})
	},
	b.escapeRegex = function(a) {
		var b = ["/", ".", "*", "+", "?", "|", "(", ")", "[", "]", "{", "}", "\\", "$", "^"];
		return a.replace(new RegExp("(\\" + b.join("|\\") + ")", "gim"), "\\$1")
	},
	b.keyCode = {
		ALT: 18,
		BACKSPACE: 8,
		BACKSPACE_SAFARI: 127,
		CAPS_LOCK: 20,
		COMMA: 188,
		COMMAND: 91,
		COMMAND_LEFT: 91,
		COMMAND_RIGHT: 93,
		CONTROL: 17,
		DELETE: 46,
		DOWN: 40,
		END: 35,
		ENTER: 13,
		ESCAPE: 27,
		HOME: 36,
		INSERT: 45,
		LEFT: 37,
		MENU: 93,
		NUMPAD_ADD: 107,
		NUMPAD_DECIMAL: 110,
		NUMPAD_DIVIDE: 111,
		NUMPAD_ENTER: 108,
		NUMPAD_MULTIPLY: 106,
		NUMPAD_SUBTRACT: 109,
		PAGE_DOWN: 34,
		PAGE_UP: 33,
		PERIOD: 190,
		RIGHT: 39,
		SHIFT: 16,
		SPACE: 32,
		TAB: 9,
		UP: 38,
		WINDOWS: 91,
		X: 88
	};
	var i = navigator.userAgent,
		j = /mobile/i.test(i),
		k = /iemobile/i.test(i),
		l = /iphone/i.test(i) && !k;
	return window.Inputmask = b, b
}(jQuery),
function(a, b) {
	return void 0 === a.fn.inputmask && (a.fn.inputmask = function(c, d) {
		var e,
			f = this[0];
		if (void 0 === d && (d = {}), "string" == typeof c)
			switch (c) {
			case "unmaskedvalue":
				return f && f.inputmask ? f.inputmask.unmaskedvalue() : a(f).val();
			case "remove":
				return this.each(function() {
					this.inputmask && this.inputmask.remove()
				});
			case "getemptymask":
				return f && f.inputmask ? f.inputmask.getemptymask() : "";
			case "hasMaskedValue":
				return !(!f || !f.inputmask) && f.inputmask.hasMaskedValue();
			case "isComplete":
				return !f || !f.inputmask || f.inputmask.isComplete();
			case "getmetadata":
				return f && f.inputmask ? f.inputmask.getmetadata() : void 0;
			case "setvalue":
				a(f).val(d),
				f && void 0 === f.inputmask && a(f).triggerHandler("setvalue");
				break;
			case "option":
				if ("string" != typeof d)
					return this.each(function() {
						if (void 0 !== this.inputmask)
							return this.inputmask.option(d)
					});
				if (f && void 0 !== f.inputmask)
					return f.inputmask.option(d);
				break;
			default:
				return d.alias = c, e = new b(d), this.each(function() {
					e.mask(this)
				})
			}
		else {
			if ("object" == typeof c)
				return e = new b(c), void 0 === c.mask && void 0 === c.alias ? this.each(function() {
					return void 0 !== this.inputmask ? this.inputmask.option(c) : void e.mask(this)
				}) : this.each(function() {
					e.mask(this)
				});
			if (void 0 === c)
				return this.each(function() {
					e = new b(d),
					e.mask(this)
				})
		}
	}), a.fn.inputmask
}(jQuery, Inputmask),
function(a, b) {
	return b.extendDefinitions({
		h: {
			validator: "[01][0-9]|2[0-3]",
			cardinality: 2,
			prevalidator: [{
				validator: "[0-2]",
				cardinality: 1
			}]
		},
		s: {
			validator: "[0-5][0-9]",
			cardinality: 2,
			prevalidator: [{
				validator: "[0-5]",
				cardinality: 1
			}]
		},
		d: {
			validator: "0[1-9]|[12][0-9]|3[01]",
			cardinality: 2,
			prevalidator: [{
				validator: "[0-3]",
				cardinality: 1
			}]
		},
		m: {
			validator: "0[1-9]|1[012]",
			cardinality: 2,
			prevalidator: [{
				validator: "[01]",
				cardinality: 1
			}]
		},
		y: {
			validator: "(19|20)\\d{2}",
			cardinality: 4,
			prevalidator: [{
				validator: "[12]",
				cardinality: 1
			}, {
				validator: "(19|20)",
				cardinality: 2
			}, {
				validator: "(19|20)\\d",
				cardinality: 3
			}]
		}
	}), b.extendAliases({
		"dd/mm/yyyy": {
			mask: "1/2/y",
			placeholder: "dd/mm/yyyy",
			regex: {
				val1pre: new RegExp("[0-3]"),
				val1: new RegExp("0[1-9]|[12][0-9]|3[01]"),
				val2pre: function(a) {
					var c = b.escapeRegex.call(this, a);
					return new RegExp("((0[1-9]|[12][0-9]|3[01])" + c + "[01])")
				},
				val2: function(a) {
					var c = b.escapeRegex.call(this, a);
					return new RegExp("((0[1-9]|[12][0-9])" + c + "(0[1-9]|1[012]))|(30" + c + "(0[13-9]|1[012]))|(31" + c + "(0[13578]|1[02]))")
				}
			},
			leapday: "29/02/",
			separator: "/",
			yearrange: {
				minyear: 1900,
				maxyear: 2099
			},
			isInYearRange: function(a, b, c) {
				if (isNaN(a))
					return !1;
				var d = parseInt(a.concat(b.toString().slice(a.length))),
					e = parseInt(a.concat(c.toString().slice(a.length)));
				return !isNaN(d) && (b <= d && d <= c) || !isNaN(e) && (b <= e && e <= c)
			},
			determinebaseyear: function(a, b, c) {
				var d = (new Date).getFullYear();
				if (a > d)
					return a;
				if (b < d) {
					for (var e = b.toString().slice(0, 2), f = b.toString().slice(2, 4); b < e + c;)
						e--;
					var g = e + f;
					return a > g ? a : g
				}
				if (a <= d && d <= b) {
					for (var h = d.toString().slice(0, 2); b < h + c;)
						h--;
					var i = h + c;
					return i < a ? a : i
				}
				return d
			},
			onKeyDown: function(c, d, e, f) {
				var g = a(this);
				if (c.ctrlKey && c.keyCode === b.keyCode.RIGHT) {
					var h = new Date;
					g.val(h.getDate().toString() + (h.getMonth() + 1).toString() + h.getFullYear().toString()),
					g.trigger("setvalue")
				}
			},
			getFrontValue: function(a, b, c) {
				for (var d = 0, e = 0, f = 0; f < a.length && "2" !== a.charAt(f); f++) {
					var g = c.definitions[a.charAt(f)];
					g ? (d += e, e = g.cardinality) : e++
				}
				return b.join("").substr(d, e)
			},
			definitions: {
				1: {
					validator: function(a, b, c, d, e) {
						var f = e.regex.val1.test(a);
						return d || f || a.charAt(1) !== e.separator && "-./".indexOf(a.charAt(1)) === -1 || !(f = e.regex.val1.test("0" + a.charAt(0))) ? f : (b.buffer[c - 1] = "0", {
							refreshFromBuffer: {
								start: c - 1,
								end: c
							},
							pos: c,
							c: a.charAt(0)
						})
					},
					cardinality: 2,
					prevalidator: [{
						validator: function(a, b, c, d, e) {
							var f = a;
							isNaN(b.buffer[c + 1]) || (f += b.buffer[c + 1]);
							var g = 1 === f.length ? e.regex.val1pre.test(f) : e.regex.val1.test(f);
							if (!d && !g) {
								if (g = e.regex.val1.test(a + "0"))
									return b.buffer[c] = a, b.buffer[++c] = "0", {
										pos: c,
										c: "0"
									};
								if (g = e.regex.val1.test("0" + a))
									return b.buffer[c] = "0", c++, {
										pos: c
									}
							}
							return g
						},
						cardinality: 1
					}]
				},
				2: {
					validator: function(a, b, c, d, e) {
						var f = e.getFrontValue(b.mask, b.buffer, e);
						f.indexOf(e.placeholder[0]) !== -1 && (f = "01" + e.separator);
						var g = e.regex.val2(e.separator).test(f + a);
						if (!d && !g && (a.charAt(1) === e.separator || "-./".indexOf(a.charAt(1)) !== -1) && (g = e.regex.val2(e.separator).test(f + "0" + a.charAt(0))))
							return b.buffer[c - 1] = "0", {
								refreshFromBuffer: {
									start: c - 1,
									end: c
								},
								pos: c,
								c: a.charAt(0)
							};
						if (e.mask.indexOf("2") === e.mask.length - 1 && g) {
							var h = b.buffer.join("").substr(4, 4) + a;
							if (h !== e.leapday)
								return !0;
							var i = parseInt(b.buffer.join("").substr(0, 4), 10);
							return i % 4 === 0 && (i % 100 !== 0 || i % 400 === 0)
						}
						return g
					},
					cardinality: 2,
					prevalidator: [{
						validator: function(a, b, c, d, e) {
							isNaN(b.buffer[c + 1]) || (a += b.buffer[c + 1]);
							var f = e.getFrontValue(b.mask, b.buffer, e);
							f.indexOf(e.placeholder[0]) !== -1 && (f = "01" + e.separator);
							var g = 1 === a.length ? e.regex.val2pre(e.separator).test(f + a) : e.regex.val2(e.separator).test(f + a);
							return d || g || !(g = e.regex.val2(e.separator).test(f + "0" + a)) ? g : (b.buffer[c] = "0", c++, {
								pos: c
							})
						},
						cardinality: 1
					}]
				},
				y: {
					validator: function(a, b, c, d, e) {
						if (e.isInYearRange(a, e.yearrange.minyear, e.yearrange.maxyear)) {
							var f = b.buffer.join("").substr(0, 6);
							if (f !== e.leapday)
								return !0;
							var g = parseInt(a, 10);
							return g % 4 === 0 && (g % 100 !== 0 || g % 400 === 0)
						}
						return !1
					},
					cardinality: 4,
					prevalidator: [{
						validator: function(a, b, c, d, e) {
							var f = e.isInYearRange(a, e.yearrange.minyear, e.yearrange.maxyear);
							if (!d && !f) {
								var g = e.determinebaseyear(e.yearrange.minyear, e.yearrange.maxyear, a + "0").toString().slice(0, 1);
								if (f = e.isInYearRange(g + a, e.yearrange.minyear, e.yearrange.maxyear))
									return b.buffer[c++] = g.charAt(0), {
										pos: c
									};
								if (g = e.determinebaseyear(e.yearrange.minyear, e.yearrange.maxyear, a + "0").toString().slice(0, 2), f = e.isInYearRange(g + a, e.yearrange.minyear, e.yearrange.maxyear))
									return b.buffer[c++] = g.charAt(0), b.buffer[c++] = g.charAt(1), {
										pos: c
									}
							}
							return f
						},
						cardinality: 1
					}, {
						validator: function(a, b, c, d, e) {
							var f = e.isInYearRange(a, e.yearrange.minyear, e.yearrange.maxyear);
							if (!d && !f) {
								var g = e.determinebaseyear(e.yearrange.minyear, e.yearrange.maxyear, a).toString().slice(0, 2);
								if (f = e.isInYearRange(a[0] + g[1] + a[1], e.yearrange.minyear, e.yearrange.maxyear))
									return b.buffer[c++] = g.charAt(1), {
										pos: c
									};
								if (g = e.determinebaseyear(e.yearrange.minyear, e.yearrange.maxyear, a).toString().slice(0, 2), e.isInYearRange(g + a, e.yearrange.minyear, e.yearrange.maxyear)) {
									var h = b.buffer.join("").substr(0, 6);
									if (h !== e.leapday)
										f = !0;
									else {
										var i = parseInt(a, 10);
										f = i % 4 === 0 && (i % 100 !== 0 || i % 400 === 0)
									}
								} else
									f = !1;
								if (f)
									return b.buffer[c - 1] = g.charAt(0), b.buffer[c++] = g.charAt(1), b.buffer[c++] = a.charAt(0), {
										refreshFromBuffer: {
											start: c - 3,
											end: c
										},
										pos: c
									}
							}
							return f
						},
						cardinality: 2
					}, {
						validator: function(a, b, c, d, e) {
							return e.isInYearRange(a, e.yearrange.minyear, e.yearrange.maxyear)
						},
						cardinality: 3
					}]
				}
			},
			insertMode: !1,
			autoUnmask: !1
		},
		"mm/dd/yyyy": {
			placeholder: "mm/dd/yyyy",
			alias: "dd/mm/yyyy",
			regex: {
				val2pre: function(a) {
					var c = b.escapeRegex.call(this, a);
					return new RegExp("((0[13-9]|1[012])" + c + "[0-3])|(02" + c + "[0-2])")
				},
				val2: function(a) {
					var c = b.escapeRegex.call(this, a);
					return new RegExp("((0[1-9]|1[012])" + c + "(0[1-9]|[12][0-9]))|((0[13-9]|1[012])" + c + "30)|((0[13578]|1[02])" + c + "31)")
				},
				val1pre: new RegExp("[01]"),
				val1: new RegExp("0[1-9]|1[012]")
			},
			leapday: "02/29/",
			onKeyDown: function(c, d, e, f) {
				var g = a(this);
				if (c.ctrlKey && c.keyCode === b.keyCode.RIGHT) {
					var h = new Date;
					g.val((h.getMonth() + 1).toString() + h.getDate().toString() + h.getFullYear().toString()),
					g.trigger("setvalue")
				}
			}
		},
		"yyyy/mm/dd": {
			mask: "y/1/2",
			placeholder: "yyyy/mm/dd",
			alias: "mm/dd/yyyy",
			leapday: "/02/29",
			onKeyDown: function(c, d, e, f) {
				var g = a(this);
				if (c.ctrlKey && c.keyCode === b.keyCode.RIGHT) {
					var h = new Date;
					g.val(h.getFullYear().toString() + (h.getMonth() + 1).toString() + h.getDate().toString()),
					g.trigger("setvalue")
				}
			}
		},
		"dd.mm.yyyy": {
			mask: "1.2.y",
			placeholder: "dd.mm.yyyy",
			leapday: "29.02.",
			separator: ".",
			alias: "dd/mm/yyyy"
		},
		"dd-mm-yyyy": {
			mask: "1-2-y",
			placeholder: "dd-mm-yyyy",
			leapday: "29-02-",
			separator: "-",
			alias: "dd/mm/yyyy"
		},
		"mm.dd.yyyy": {
			mask: "1.2.y",
			placeholder: "mm.dd.yyyy",
			leapday: "02.29.",
			separator: ".",
			alias: "mm/dd/yyyy"
		},
		"mm-dd-yyyy": {
			mask: "1-2-y",
			placeholder: "mm-dd-yyyy",
			leapday: "02-29-",
			separator: "-",
			alias: "mm/dd/yyyy"
		},
		"yyyy.mm.dd": {
			mask: "y.1.2",
			placeholder: "yyyy.mm.dd",
			leapday: ".02.29",
			separator: ".",
			alias: "yyyy/mm/dd"
		},
		"yyyy-mm-dd": {
			mask: "y-1-2",
			placeholder: "yyyy-mm-dd",
			leapday: "-02-29",
			separator: "-",
			alias: "yyyy/mm/dd"
		},
		datetime: {
			mask: "1/2/y h:s",
			placeholder: "dd/mm/yyyy hh:mm",
			alias: "dd/mm/yyyy",
			regex: {
				hrspre: new RegExp("[012]"),
				hrs24: new RegExp("2[0-4]|1[3-9]"),
				hrs: new RegExp("[01][0-9]|2[0-4]"),
				ampm: new RegExp("^[a|p|A|P][m|M]"),
				mspre: new RegExp("[0-5]"),
				ms: new RegExp("[0-5][0-9]")
			},
			timeseparator: ":",
			hourFormat: "24",
			definitions: {
				h: {
					validator: function(a, b, c, d, e) {
						if ("24" === e.hourFormat && 24 === parseInt(a, 10))
							return b.buffer[c - 1] = "0", b.buffer[c] = "0", {
								refreshFromBuffer: {
									start: c - 1,
									end: c
								},
								c: "0"
							};
						var f = e.regex.hrs.test(a);
						if (!d && !f && (a.charAt(1) === e.timeseparator || "-.:".indexOf(a.charAt(1)) !== -1) && (f = e.regex.hrs.test("0" + a.charAt(0))))
							return b.buffer[c - 1] = "0", b.buffer[c] = a.charAt(0), c++, {
								refreshFromBuffer: {
									start: c - 2,
									end: c
								},
								pos: c,
								c: e.timeseparator
							};
						if (f && "24" !== e.hourFormat && e.regex.hrs24.test(a)) {
							var g = parseInt(a, 10);
							return 24 === g ? (b.buffer[c + 5] = "a", b.buffer[c + 6] = "m") : (b.buffer[c + 5] = "p", b.buffer[c + 6] = "m"), g -= 12, g < 10 ? (b.buffer[c] = g.toString(), b.buffer[c - 1] = "0") : (b.buffer[c] = g.toString().charAt(1), b.buffer[c - 1] = g.toString().charAt(0)), {
								refreshFromBuffer: {
									start: c - 1,
									end: c + 6
								},
								c: b.buffer[c]
							}
						}
						return f
					},
					cardinality: 2,
					prevalidator: [{
						validator: function(a, b, c, d, e) {
							var f = e.regex.hrspre.test(a);
							return d || f || !(f = e.regex.hrs.test("0" + a)) ? f : (b.buffer[c] = "0", c++, {
								pos: c
							})
						},
						cardinality: 1
					}]
				},
				s: {
					validator: "[0-5][0-9]",
					cardinality: 2,
					prevalidator: [{
						validator: function(a, b, c, d, e) {
							var f = e.regex.mspre.test(a);
							return d || f || !(f = e.regex.ms.test("0" + a)) ? f : (b.buffer[c] = "0", c++, {
								pos: c
							})
						},
						cardinality: 1
					}]
				},
				t: {
					validator: function(a, b, c, d, e) {
						return e.regex.ampm.test(a + "m")
					},
					casing: "lower",
					cardinality: 1
				}
			},
			insertMode: !1,
			autoUnmask: !1
		},
		datetime12: {
			mask: "1/2/y h:s t\\m",
			placeholder: "dd/mm/yyyy hh:mm xm",
			alias: "datetime",
			hourFormat: "12"
		},
		"mm/dd/yyyy hh:mm xm": {
			mask: "1/2/y h:s t\\m",
			placeholder: "mm/dd/yyyy hh:mm xm",
			alias: "datetime12",
			regex: {
				val2pre: function(a) {
					var c = b.escapeRegex.call(this, a);
					return new RegExp("((0[13-9]|1[012])" + c + "[0-3])|(02" + c + "[0-2])")
				},
				val2: function(a) {
					var c = b.escapeRegex.call(this, a);
					return new RegExp("((0[1-9]|1[012])" + c + "(0[1-9]|[12][0-9]))|((0[13-9]|1[012])" + c + "30)|((0[13578]|1[02])" + c + "31)")
				},
				val1pre: new RegExp("[01]"),
				val1: new RegExp("0[1-9]|1[012]")
			},
			leapday: "02/29/",
			onKeyDown: function(c, d, e, f) {
				var g = a(this);
				if (c.ctrlKey && c.keyCode === b.keyCode.RIGHT) {
					var h = new Date;
					g.val((h.getMonth() + 1).toString() + h.getDate().toString() + h.getFullYear().toString()),
					g.trigger("setvalue")
				}
			}
		},
		"hh:mm t": {
			mask: "h:s t\\m",
			placeholder: "hh:mm xm",
			alias: "datetime",
			hourFormat: "12"
		},
		"h:s t": {
			mask: "h:s t\\m",
			placeholder: "hh:mm xm",
			alias: "datetime",
			hourFormat: "12"
		},
		"hh:mm:ss": {
			mask: "h:s:s",
			placeholder: "hh:mm:ss",
			alias: "datetime",
			autoUnmask: !1
		},
		"hh:mm": {
			mask: "h:s",
			placeholder: "hh:mm",
			alias: "datetime",
			autoUnmask: !1
		},
		date: {
			alias: "dd/mm/yyyy"
		},
		"mm/yyyy": {
			mask: "1/y",
			placeholder: "mm/yyyy",
			leapday: "donotuse",
			separator: "/",
			alias: "mm/dd/yyyy"
		},
		shamsi: {
			regex: {
				val2pre: function(a) {
					var c = b.escapeRegex.call(this, a);
					return new RegExp("((0[1-9]|1[012])" + c + "[0-3])")
				},
				val2: function(a) {
					var c = b.escapeRegex.call(this, a);
					return new RegExp("((0[1-9]|1[012])" + c + "(0[1-9]|[12][0-9]))|((0[1-9]|1[012])" + c + "30)|((0[1-6])" + c + "31)")
				},
				val1pre: new RegExp("[01]"),
				val1: new RegExp("0[1-9]|1[012]")
			},
			yearrange: {
				minyear: 1300,
				maxyear: 1499
			},
			mask: "y/1/2",
			leapday: "/12/30",
			placeholder: "yyyy/mm/dd",
			alias: "mm/dd/yyyy",
			clearIncomplete: !0
		}
	}), b
}(jQuery, Inputmask),
function(a, b) {
	return b.extendDefinitions({
		A: {
			validator: "[A-Za-z\u0410-\u044f\u0401\u0451\xc0-\xff\xb5]",
			cardinality: 1,
			casing: "upper"
		},
		"&": {
			validator: "[0-9A-Za-z\u0410-\u044f\u0401\u0451\xc0-\xff\xb5]",
			cardinality: 1,
			casing: "upper"
		},
		"#": {
			validator: "[0-9A-Fa-f]",
			cardinality: 1,
			casing: "upper"
		}
	}), b.extendAliases({
		url: {
			definitions: {
				i: {
					validator: ".",
					cardinality: 1
				}
			},
			mask: "(\\http://)|(\\http\\s://)|(ftp://)|(ftp\\s://)i{+}",
			insertMode: !1,
			autoUnmask: !1
		},
		ip: {
			mask: "i[i[i]].i[i[i]].i[i[i]].i[i[i]]",
			definitions: {
				i: {
					validator: function(a, b, c, d, e) {
						return c - 1 > -1 && "." !== b.buffer[c - 1] ? (a = b.buffer[c - 1] + a, a = c - 2 > -1 && "." !== b.buffer[c - 2] ? b.buffer[c - 2] + a : "0" + a) : a = "00" + a, new RegExp("25[0-5]|2[0-4][0-9]|[01][0-9][0-9]").test(a)
					},
					cardinality: 1
				}
			},
			onUnMask: function(a, b, c) {
				return a
			}
		},
		email: {
			mask: "*{1,64}[.*{1,64}][.*{1,64}][.*{1,63}]@-{1,63}.-{1,63}[.-{1,63}][.-{1,63}]",
			greedy: !1,
			onBeforePaste: function(a, b) {
				return a = a.toLowerCase(), a.replace("mailto:", "")
			},
			definitions: {
				"*": {
					validator: "[0-9A-Za-z!#$%&'*+/=?^_`{|}~-]",
					cardinality: 1,
					casing: "lower"
				},
				"-": {
					validator: "[0-9A-Za-z-]",
					cardinality: 1,
					casing: "lower"
				}
			},
			onUnMask: function(a, b, c) {
				return a
			}
		},
		mac: {
			mask: "##:##:##:##:##:##"
		},
		vin: {
			mask: "V{13}9{4}",
			definitions: {
				V: {
					validator: "[A-HJ-NPR-Za-hj-npr-z\\d]",
					cardinality: 1,
					casing: "upper"
				}
			},
			clearIncomplete: !0,
			autoUnmask: !0
		}
	}), b
}(jQuery, Inputmask),
function(a, b) {
	return b.extendAliases({
		numeric: {
			mask: function(a) {
				function c(b) {
					for (var c = "", d = 0; d < b.length; d++)
						c += a.definitions[b.charAt(d)] || a.optionalmarker.start === b.charAt(d) || a.optionalmarker.end === b.charAt(d) || a.quantifiermarker.start === b.charAt(d) || a.quantifiermarker.end === b.charAt(d) || a.groupmarker.start === b.charAt(d) || a.groupmarker.end === b.charAt(d) || a.alternatormarker === b.charAt(d) ? "\\" + b.charAt(d) : b.charAt(d);
					return c
				}
				if (0 !== a.repeat && isNaN(a.integerDigits) && (a.integerDigits = a.repeat), a.repeat = 0, a.groupSeparator === a.radixPoint && ("." === a.radixPoint ? a.groupSeparator = "," : "," === a.radixPoint ? a.groupSeparator = "." : a.groupSeparator = ""), " " === a.groupSeparator && (a.skipOptionalPartCharacter = void 0), a.autoGroup = a.autoGroup && "" !== a.groupSeparator, a.autoGroup && ("string" == typeof a.groupSize && isFinite(a.groupSize) && (a.groupSize = parseInt(a.groupSize)), isFinite(a.integerDigits))) {
					var d = Math.floor(a.integerDigits / a.groupSize),
						e = a.integerDigits % a.groupSize;
					a.integerDigits = parseInt(a.integerDigits) + (0 === e ? d - 1 : d),
					a.integerDigits < 1 && (a.integerDigits = "*")
				}
				a.placeholder.length > 1 && (a.placeholder = a.placeholder.charAt(0)),
				"radixFocus" === a.positionCaretOnClick && "" === a.placeholder && a.integerOptional === !1 && (a.positionCaretOnClick = "lvp"),
				a.definitions[";"] = a.definitions["~"],
				a.definitions[";"].definitionSymbol = "~",
				a.numericInput === !0 && (a.positionCaretOnClick = "radixFocus" === a.positionCaretOnClick ? "lvp" : a.positionCaretOnClick, a.digitsOptional = !1, isNaN(a.digits) && (a.digits = 2), a.decimalProtect = !1);
				var f = c(a.prefix);
				if (f += "[+]", f += a.integerOptional === !0 ? "~{1," + a.integerDigits + "}" : "~{" + a.integerDigits + "}", void 0 !== a.digits) {
					a.decimalProtect && (a.radixPointDefinitionSymbol = ":");
					var g = a.digits.toString().split(",");
					isFinite(g[0] && g[1] && isFinite(g[1])) ? f += (a.decimalProtect ? ":" : a.radixPoint) + ";{" + a.digits + "}" : (isNaN(a.digits) || parseInt(a.digits) > 0) && (f += a.digitsOptional ? "[" + (a.decimalProtect ? ":" : a.radixPoint) + ";{1," + a.digits + "}]" : (a.decimalProtect ? ":" : a.radixPoint) + ";{" + a.digits + "}")
				}
				return f += "[-]", f += c(a.suffix), a.greedy = !1, null !== a.min && (a.min = a.min.toString().replace(new RegExp(b.escapeRegex(a.groupSeparator), "g"), ""), "," === a.radixPoint && (a.min = a.min.replace(a.radixPoint, "."))), null !== a.max && (a.max = a.max.toString().replace(new RegExp(b.escapeRegex(a.groupSeparator), "g"), ""), "," === a.radixPoint && (a.max = a.max.replace(a.radixPoint, "."))), f
			},
			placeholder: "",
			greedy: !1,
			digits: "*",
			digitsOptional: !0,
			radixPoint: ".",
			positionCaretOnClick: "radixFocus",
			groupSize: 3,
			groupSeparator: "",
			autoGroup: !1,
			allowPlus: !0,
			allowMinus: !0,
			negationSymbol: {
				front: "-",
				back: ""
			},
			integerDigits: "+",
			integerOptional: !0,
			prefix: "",
			suffix: "",
			rightAlign: !0,
			decimalProtect: !0,
			min: null,
			max: null,
			step: 1,
			insertMode: !0,
			autoUnmask: !1,
			unmaskAsNumber: !1,
			postFormat: function(c, d, e) {
				e.numericInput === !0 && (c = c.reverse(), isFinite(d) && (d = c.join("").length - d - 1));
				var f,
					g;
				d = d >= c.length ? c.length - 1 : d < e.prefix.length ? e.prefix.length : d;
				var h = c[d],
					i = c.slice();
				h === e.groupSeparator && (i.splice(d--, 1), h = i[d]),
				i[d] = "!";
				var j = i.join(""),
					k = j;
				if (j = j.replace(new RegExp(b.escapeRegex(e.suffix) + "$"), ""), j = j.replace(new RegExp("^" + b.escapeRegex(e.prefix)), ""), j.length > 0 && e.autoGroup || j.indexOf(e.groupSeparator) !== -1) {
					var l = b.escapeRegex(e.groupSeparator);
					j = j.replace(new RegExp(l, "g"), "");
					var m = j.split(h === e.radixPoint ? "!" : e.radixPoint);
					if (j = "" === e.radixPoint ? j : m[0], h !== e.negationSymbol.front && (j = j.replace("!", "?")), j.length > e.groupSize)
						for (var n = new RegExp("([-+]?[\\d?]+)([\\d?]{" + e.groupSize + "})"); n.test(j) && "" !== e.groupSeparator;)
							j = j.replace(n, "$1" + e.groupSeparator + "$2"),
							j = j.replace(e.groupSeparator + e.groupSeparator, e.groupSeparator);
					j = j.replace("?", "!"),
					"" !== e.radixPoint && m.length > 1 && (j += (h === e.radixPoint ? "!" : e.radixPoint) + m[1])
				}
				j = e.prefix + j + e.suffix;
				var o = k !== j;
				if (o)
					for (c.length = j.length, f = 0, g = j.length; f < g; f++)
						c[f] = j.charAt(f);
				var p = a.inArray("!", j);
				return c[p] = h, p = e.numericInput && isFinite(d) ? c.join("").length - p - 1 : p, e.numericInput && (c = c.reverse(), a.inArray(e.radixPoint, c) < p && c.join("").length - e.suffix.length !== p && (p -= 1)), {
					pos: p,
					refreshFromBuffer: o,
					buffer: c
				}
			},
			onBeforeWrite: function(c, d, e, f) {
				var g;
				if (c && ("blur" === c.type || "checkval" === c.type || "keydown" === c.type)) {
					var h = f.numericInput ? d.slice().reverse().join("") : d.join(""),
						i = h.replace(f.prefix, "");
					i = i.replace(f.suffix, ""),
					i = i.replace(new RegExp(b.escapeRegex(f.groupSeparator), "g"), ""),
					"," === f.radixPoint && (i = i.replace(f.radixPoint, "."));
					var j = i.match(new RegExp("[-" + b.escapeRegex(f.negationSymbol.front) + "]", "g"));
					if (j = null !== j && 1 === j.length, i = i.replace(new RegExp("[-" + b.escapeRegex(f.negationSymbol.front) + "]", "g"), ""), i = i.replace(new RegExp(b.escapeRegex(f.negationSymbol.back) + "$"), ""), isNaN(f.placeholder) && (i = i.replace(new RegExp(b.escapeRegex(f.placeholder), "g"), "")), i = i === f.negationSymbol.front ? i + "0" : i, "" !== i && isFinite(i)) {
						var k = parseFloat(i),
							l = j ? k * -1 : k;
						if (null !== f.min && isFinite(f.min) && l < parseFloat(f.min) ? (k = Math.abs(f.min), j = f.min < 0, h = void 0) : null !== f.max && isFinite(f.max) && l > parseFloat(f.max) && (k = Math.abs(f.max), j = f.max < 0, h = void 0), i = k.toString().replace(".", f.radixPoint).split(""), isFinite(f.digits)) {
							var m = a.inArray(f.radixPoint, i),
								n = a.inArray(f.radixPoint, h);
							m === -1 && (i.push(f.radixPoint), m = i.length - 1);
							for (var o = 1; o <= f.digits; o++)
								f.digitsOptional || void 0 !== i[m + o] && i[m + o] !== f.placeholder.charAt(0) ? n !== -1 && void 0 !== h[n + o] && (i[m + o] = i[m + o] || h[n + o]) : i[m + o] = "0";
							i[i.length - 1] === f.radixPoint && delete i[i.length - 1]
						}
						if (k.toString() !== i && k.toString() + "." !== i || j)
							return !j || 0 === k && "blur" === c.type || (i.unshift(f.negationSymbol.front), i.push(f.negationSymbol.back)), i = (f.prefix + i.join("")).split(""), f.numericInput && (i = i.reverse()), g = f.postFormat(i, f.numericInput ? e : e - 1, f), g.buffer && (g.refreshFromBuffer = g.buffer.join("") !== d.join("")), g
					}
				}
				if (f.autoGroup)
					return g = f.postFormat(d, f.numericInput ? e : e - 1, f), g.caret = e <= f.prefix.length ? g.pos : g.pos + 1, g
			},
			regex: {
				integerPart: function(a) {
					return new RegExp("[" + b.escapeRegex(a.negationSymbol.front) + "+]?\\d+")
				},
				integerNPart: function(a) {
					return new RegExp("[\\d" + b.escapeRegex(a.groupSeparator) + b.escapeRegex(a.placeholder.charAt(0)) + "]+")
				}
			},
			signHandler: function(a, b, c, d, e) {
				if (!d && e.allowMinus && "-" === a || e.allowPlus && "+" === a) {
					var f = b.buffer.join("").match(e.regex.integerPart(e));
					if (f && f[0].length > 0)
						return b.buffer[f.index] === ("-" === a ? "+" : e.negationSymbol.front) ? "-" === a ? "" !== e.negationSymbol.back ? {
							pos: f.index,
							c: e.negationSymbol.front,
							remove: f.index,
							caret: c,
							insert: {
								pos: b.buffer.length - e.suffix.length - 1,
								c: e.negationSymbol.back
							}
						} : {
							pos: f.index,
							c: e.negationSymbol.front,
							remove: f.index,
							caret: c
						} : "" !== e.negationSymbol.back ? {
							pos: f.index,
							c: "+",
							remove: [f.index, b.buffer.length - e.suffix.length - 1],
							caret: c
						} : {
							pos: f.index,
							c: "+",
							remove: f.index,
							caret: c
						} : b.buffer[f.index] === ("-" === a ? e.negationSymbol.front : "+") ? "-" === a && "" !== e.negationSymbol.back ? {
							remove: [f.index, b.buffer.length - e.suffix.length - 1],
							caret: c - 1
						} : {
							remove: f.index,
							caret: c - 1
						} : "-" === a ? "" !== e.negationSymbol.back ? {
							pos: f.index,
							c: e.negationSymbol.front,
							caret: c + 1,
							insert: {
								pos: b.buffer.length - e.suffix.length,
								c: e.negationSymbol.back
							}
						} : {
							pos: f.index,
							c: e.negationSymbol.front,
							caret: c + 1
						} : {
							pos: f.index,
							c: a,
							caret: c + 1
						}
				}
				return !1
			},
			radixHandler: function(b, c, d, e, f) {
				if (!e && f.numericInput !== !0 && b === f.radixPoint && void 0 !== f.digits && (isNaN(f.digits) || parseInt(f.digits) > 0)) {
					var g = a.inArray(f.radixPoint, c.buffer),
						h = c.buffer.join("").match(f.regex.integerPart(f));
					if (g !== -1 && c.validPositions[g])
						return c.validPositions[g - 1] ? {
							caret: g + 1
						} : {
							pos: h.index,
							c: h[0],
							caret: g + 1
						};
					if (!h || "0" === h[0] && h.index + 1 !== d)
						return c.buffer[h ? h.index : d] = "0", {
							pos: (h ? h.index : d) + 1,
							c: f.radixPoint
						}
				}
				return !1
			},
			leadingZeroHandler: function(b, c, d, e, f, g) {
				if (!e) {
					var h = c.buffer.slice("");
					if (h.splice(0, f.prefix.length), h.splice(h.length - f.suffix.length, f.suffix.length), f.numericInput === !0) {
						var h = h.reverse(),
							i = h[0];
						if ("0" === i && void 0 === c.validPositions[d - 1])
							return {
								pos: d,
								remove: h.length - 1
							}
					} else {
						d -= f.prefix.length;
						var j = a.inArray(f.radixPoint, h),
							k = h.slice(0, j !== -1 ? j : void 0).join("").match(f.regex.integerNPart(f));
						if (k && (j === -1 || d <= j)) {
							var l = j === -1 ? 0 : parseInt(h.slice(j + 1).join(""));
							if (0 === k[0].indexOf("" !== f.placeholder ? f.placeholder.charAt(0) : "0") && (k.index + 1 === d || g !== !0 && 0 === l))
								return c.buffer.splice(k.index + f.prefix.length, 1), {
									pos: k.index + f.prefix.length,
									remove: k.index + f.prefix.length
								};
							if ("0" === b && d <= k.index && k[0] !== f.groupSeparator)
								return !1
						}
					}
				}
				return !0
			},
			definitions: {
				"~": {
					validator: function(c, d, e, f, g, h) {
						var i = g.signHandler(c, d, e, f, g);
						if (!i && (i = g.radixHandler(c, d, e, f, g), !i && (i = f ? new RegExp("[0-9" + b.escapeRegex(g.groupSeparator) + "]").test(c) : new RegExp("[0-9]").test(c), i === !0 && (i = g.leadingZeroHandler(c, d, e, f, g, h), i === !0)))) {
							var j = a.inArray(g.radixPoint, d.buffer);
							i = j !== -1 && (g.digitsOptional === !1 || d.validPositions[e]) && g.numericInput !== !0 && e > j && !f ? {
								pos: e,
								remove: e
							} : {
								pos: e
							}
						}
						return i
					},
					cardinality: 1
				},
				"+": {
					validator: function(a, b, c, d, e) {
						var f = e.signHandler(a, b, c, d, e);
						return !f && (d && e.allowMinus && a === e.negationSymbol.front || e.allowMinus && "-" === a || e.allowPlus && "+" === a) && (f = !(!d && "-" === a) || ("" !== e.negationSymbol.back ? {
							pos: c,
							c: "-" === a ? e.negationSymbol.front : "+",
							caret: c + 1,
							insert: {
								pos: b.buffer.length,
								c: e.negationSymbol.back
							}
						} : {
							pos: c,
							c: "-" === a ? e.negationSymbol.front : "+",
							caret: c + 1
						})), f
					},
					cardinality: 1,
					placeholder: ""
				},
				"-": {
					validator: function(a, b, c, d, e) {
						var f = e.signHandler(a, b, c, d, e);
						return !f && d && e.allowMinus && a === e.negationSymbol.back && (f = !0), f
					},
					cardinality: 1,
					placeholder: ""
				},
				":": {
					validator: function(a, c, d, e, f) {
						var g = f.signHandler(a, c, d, e, f);
						if (!g) {
							var h = "[" + b.escapeRegex(f.radixPoint) + "]";
							g = new RegExp(h).test(a),
							g && c.validPositions[d] && c.validPositions[d].match.placeholder === f.radixPoint && (g = {
								caret: d + 1
							})
						}
						return g ? {
							c: f.radixPoint
						} : g
					},
					cardinality: 1,
					placeholder: function(a) {
						return a.radixPoint
					}
				}
			},
			onUnMask: function(a, c, d) {
				if ("" === c && d.nullable === !0)
					return c;
				var e = a.replace(d.prefix, "");
				return e = e.replace(d.suffix, ""), e = e.replace(new RegExp(b.escapeRegex(d.groupSeparator), "g"), ""), d.unmaskAsNumber ? ("" !== d.radixPoint && e.indexOf(d.radixPoint) !== -1 && (e = e.replace(b.escapeRegex.call(this, d.radixPoint), ".")), Number(e)) : e
			},
			isComplete: function(a, c) {
				var d = a.join(""),
					e = a.slice();
				if (c.postFormat(e, 0, c), e.join("") !== d)
					return !1;
				var f = d.replace(c.prefix, "");
				return f = f.replace(c.suffix, ""), f = f.replace(new RegExp(b.escapeRegex(c.groupSeparator), "g"), ""), "," === c.radixPoint && (f = f.replace(b.escapeRegex(c.radixPoint), ".")), isFinite(f)
			},
			onBeforeMask: function(a, c) {
				if (c.numericInput === !0 && (a = a.split("").reverse().join("")), "" !== c.radixPoint && isFinite(a))
					a = a.toString().replace(".", c.radixPoint);
				else {
					var d = a.match(/,/g),
						e = a.match(/\./g);
					e && d ? e.length > d.length ? (a = a.replace(/\./g, ""), a = a.replace(",", c.radixPoint)) : d.length > e.length ? (a = a.replace(/,/g, ""), a = a.replace(".", c.radixPoint)) : a = a.indexOf(".") < a.indexOf(",") ? a.replace(/\./g, "") : a = a.replace(/,/g, "") : a = a.replace(new RegExp(b.escapeRegex(c.groupSeparator), "g"), "")
				}
				if (0 === c.digits && (a.indexOf(".") !== -1 ? a = a.substring(0, a.indexOf(".")) : a.indexOf(",") !== -1 && (a = a.substring(0, a.indexOf(",")))), "" !== c.radixPoint && isFinite(c.digits) && a.indexOf(c.radixPoint) !== -1) {
					var f = a.split(c.radixPoint),
						g = f[1].match(new RegExp("\\d*"))[0];
					if (parseInt(c.digits) < g.toString().length) {
						var h = Math.pow(10, parseInt(c.digits));
						a = a.replace(b.escapeRegex(c.radixPoint), "."),
						a = Math.round(parseFloat(a) * h) / h,
						a = a.toString().replace(".", c.radixPoint)
					}
				}
				return c.numericInput === !0 && (a = a.split("").reverse().join("")), a.toString()
			},
			canClearPosition: function(a, b, c, d, e) {
				var f = a.validPositions[b].input,
					g = f !== e.radixPoint || null !== a.validPositions[b].match.fn && e.decimalProtect === !1 || isFinite(f) || b === c || f === e.groupSeparator || f === e.negationSymbol.front || f === e.negationSymbol.back;
				return g
			},
			onKeyDown: function(c, d, e, f) {
				var g = a(this);
				if (c.ctrlKey)
					switch (c.keyCode) {
					case b.keyCode.UP:
						g.val(parseFloat(this.inputmask.unmaskedvalue()) + parseInt(f.step)),
						g.trigger("setvalue");
						break;
					case b.keyCode.DOWN:
						g.val(parseFloat(this.inputmask.unmaskedvalue()) - parseInt(f.step)),
						g.trigger("setvalue")
					}
			}
		},
		currency: {
			prefix: "$ ",
			groupSeparator: ",",
			alias: "numeric",
			placeholder: "0",
			autoGroup: !0,
			digits: 2,
			digitsOptional: !1,
			clearMaskOnLostFocus: !1
		},
		decimal: {
			alias: "numeric"
		},
		integer: {
			alias: "numeric",
			digits: 0,
			radixPoint: ""
		},
		percentage: {
			alias: "numeric",
			digits: 2,
			radixPoint: ".",
			placeholder: "0",
			autoGroup: !1,
			min: 0,
			max: 100,
			suffix: " %",
			allowPlus: !1,
			allowMinus: !1
		}
	}), b
}(jQuery, Inputmask),
function(a, b) {
	return b.extendAliases({
		abstractphone: {
			countrycode: "",
			phoneCodes: [],
			mask: function(a) {
				a.definitions = {
					"#": a.definitions[9]
				};
				var b = a.phoneCodes.sort(function(a, b) {
					var c = (a.mask || a).replace(/#/g, "9").replace(/[\+\(\)#-]/g, ""),
						d = (b.mask || b).replace(/#/g, "9").replace(/[\+\(\)#-]/g, ""),
						e = (a.mask || a).split("#")[0],
						f = (b.mask || b).split("#")[0];
					return 0 === f.indexOf(e) ? -1 : 0 === e.indexOf(f) ? 1 : c.localeCompare(d)
				});
				return b
			},
			keepStatic: !0,
			onBeforeMask: function(a, b) {
				var c = a.replace(/^0{1,2}/, "").replace(/[\s]/g, "");
				return (c.indexOf(b.countrycode) > 1 || c.indexOf(b.countrycode) === -1) && (c = "+" + b.countrycode + c), c
			},
			onUnMask: function(a, b, c) {
				return b
			}
		}
	}), b
}(jQuery, Inputmask),
function(a, b) {
	return b.extendAliases({
		Regex: {
			mask: "r",
			greedy: !1,
			repeat: "*",
			regex: null,
			regexTokens: null,
			tokenizer: /\[\^?]?(?:[^\\\]]+|\\[\S\s]?)*]?|\\(?:0(?:[0-3][0-7]{0,2}|[4-7][0-7]?)?|[1-9][0-9]*|x[0-9A-Fa-f]{2}|u[0-9A-Fa-f]{4}|c[A-Za-z]|[\S\s]?)|\((?:\?[:=!]?)?|(?:[?*+]|\{[0-9]+(?:,[0-9]*)?\})\??|[^.?*+^${[()|\\]+|./g,
			quantifierFilter: /[0-9]+[^,]/,
			isComplete: function(a, b) {
				return new RegExp(b.regex).test(a.join(""))
			},
			definitions: {
				r: {
					validator: function(b, c, d, e, f) {
						function g(a, b) {
							this.matches = [],
							this.isGroup = a || !1,
							this.isQuantifier = b || !1,
							this.quantifier = {
								min: 1,
								max: 1
							},
							this.repeaterPart = void 0
						}
						function h() {
							var a,
								b,
								c = new g,
								d = [];
							for (f.regexTokens = []; a = f.tokenizer.exec(f.regex);)
								switch (b = a[0], b.charAt(0)) {
								case "(":
									d.push(new g((!0)));
									break;
								case ")":
									k = d.pop(),
									d.length > 0 ? d[d.length - 1].matches.push(k) : c.matches.push(k);
									break;
								case "{":
								case "+":
								case "*":
									var e = new g((!1), (!0));
									b = b.replace(/[{}]/g, "");
									var h = b.split(","),
										i = isNaN(h[0]) ? h[0] : parseInt(h[0]),
										j = 1 === h.length ? i : isNaN(h[1]) ? h[1] : parseInt(h[1]);
									if (e.quantifier = {
										min: i,
										max: j
									}, d.length > 0) {
										var l = d[d.length - 1].matches;
										a = l.pop(),
										a.isGroup || (k = new g((!0)), k.matches.push(a), a = k),
										l.push(a),
										l.push(e)
									} else
										a = c.matches.pop(),
										a.isGroup || (k = new g((!0)), k.matches.push(a), a = k),
										c.matches.push(a),
										c.matches.push(e);
									break;
								default:
									d.length > 0 ? d[d.length - 1].matches.push(b) : c.matches.push(b)
								}
							c.matches.length > 0 && f.regexTokens.push(c)
						}
						function i(b, c) {
							var d = !1;
							c && (m += "(", o++);
							for (var e = 0; e < b.matches.length; e++) {
								var f = b.matches[e];
								if (f.isGroup === !0)
									d = i(f, !0);
								else if (f.isQuantifier === !0) {
									var g = a.inArray(f, b.matches),
										h = b.matches[g - 1],
										k = m;
									if (isNaN(f.quantifier.max)) {
										for (; f.repeaterPart && f.repeaterPart !== m && f.repeaterPart.length > m.length && !(d = i(h, !0));)
											;
										d = d || i(h, !0),
										d && (f.repeaterPart = m),
										m = k + f.quantifier.max
									} else {
										for (var l = 0, n = f.quantifier.max - 1; l < n && !(d = i(h, !0)); l++)
											;
										m = k + "{" + f.quantifier.min + "," + f.quantifier.max + "}"
									}
								} else if (void 0 !== f.matches)
									for (var p = 0; p < f.length && !(d = i(f[p], c)); p++)
										;
								else {
									var q;
									if ("[" == f.charAt(0)) {
										q = m,
										q += f;
										for (var r = 0; r < o; r++)
											q += ")";
										var s = new RegExp("^(" + q + ")$");
										d = s.test(j)
									} else
										for (var t = 0, u = f.length; t < u; t++)
											if ("\\" !== f.charAt(t)) {
												q = m,
												q += f.substr(0, t + 1),
												q = q.replace(/\|$/, "");
												for (var r = 0; r < o; r++)
													q += ")";
												var s = new RegExp("^(" + q + ")$");
												if (d = s.test(j))
													break
											}
									m += f
								}
								if (d)
									break
							}
							return c && (m += ")", o--), d
						}
						var j,
							k,
							l = c.buffer.slice(),
							m = "",
							n = !1,
							o = 0;
						null === f.regexTokens && h(),
						l.splice(d, 0, b),
						j = l.join("");
						for (var p = 0; p < f.regexTokens.length; p++) {
							var q = f.regexTokens[p];
							if (n = i(q, q.isGroup))
								break
						}
						return n
					},
					cardinality: 1
				}
			}
		}
	}), b
}(jQuery, Inputmask);
/*
 Input Mask plugin extensions
 http://github.com/RobinHerbots/jquery.inputmask
 Copyright (c) 2010 -  Robin Herbots
 Licensed under the MIT license (http://www.opensource.org/licenses/mit-license.php)
 Version: 0.0.0-dev
 Belgian Phone extension.
 */
(function(factory) {
	if (typeof define === "function" && define.amd) {
		define(["inputmask"], factory);
	} else if (typeof exports === "object") {
		module.exports = factory(require("./inputmask"));
	} else {
		factory(window.Inputmask);
	}
}
(function(Inputmask) {
	Inputmask.extendAliases({
		"phone": {
			alias: "abstractphone",
			phoneCodes: [
			{
				"mask": "+247-####",
				"cc": "AC",
				"cd": "Ascension",
				"desc_en": "",
				"name_ru": "ÐžÑÑ‚Ñ€Ð¾Ð² Ð’Ð¾Ð·Ð½ÐµÑÐµÐ½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+376-###-###",
				"cc": "AD",
				"cd": "Andorra",
				"desc_en": "",
				"name_ru": "ÐÐ½Ð´Ð¾Ñ€Ñ€Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+971-5#-###-####",
				"cc": "AE",
				"cd": "United Arab Emirates",
				"desc_en": "mobile",
				"name_ru": "ÐžÐ±ÑŠÐµÐ´Ð¸Ð½ÐµÐ½Ð½Ñ‹Ðµ ÐÑ€Ð°Ð±ÑÐºÐ¸Ðµ Ð­Ð¼Ð¸Ñ€Ð°Ñ‚Ñ‹",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+971-#-###-####",
				"cc": "AE",
				"cd": "United Arab Emirates",
				"desc_en": "",
				"name_ru": "ÐžÐ±ÑŠÐµÐ´Ð¸Ð½ÐµÐ½Ð½Ñ‹Ðµ ÐÑ€Ð°Ð±ÑÐºÐ¸Ðµ Ð­Ð¼Ð¸Ñ€Ð°Ñ‚Ñ‹",
				"desc_ru": ""
			},
			{
				"mask": "+93-##-###-####",
				"cc": "AF",
				"cd": "Afghanistan",
				"desc_en": "",
				"name_ru": "ÐÑ„Ð³Ð°Ð½Ð¸ÑÑ‚Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+1(268)###-####",
				"cc": "AG",
				"cd": "Antigua & Barbuda",
				"desc_en": "",
				"name_ru": "ÐÐ½Ñ‚Ð¸Ð³ÑƒÐ° Ð¸ Ð‘Ð°Ñ€Ð±ÑƒÐ´Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+1(264)###-####",
				"cc": "AI",
				"cd": "Anguilla",
				"desc_en": "",
				"name_ru": "ÐÐ½Ð³Ð¸Ð»ÑŒÑ",
				"desc_ru": ""
			},
			{
				"mask": "+355(###)###-###",
				"cc": "AL",
				"cd": "Albania",
				"desc_en": "",
				"name_ru": "ÐÐ»Ð±Ð°Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+374-##-###-###",
				"cc": "AM",
				"cd": "Armenia",
				"desc_en": "",
				"name_ru": "ÐÑ€Ð¼ÐµÐ½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+599-###-####",
				"cc": "AN",
				"cd": "Caribbean Netherlands",
				"desc_en": "",
				"name_ru": "ÐšÐ°Ñ€Ð¸Ð±ÑÐºÐ¸Ðµ ÐÐ¸Ð´ÐµÑ€Ð»Ð°Ð½Ð´Ñ‹",
				"desc_ru": ""
			},
			{
				"mask": "+599-###-####",
				"cc": "AN",
				"cd": "Netherlands Antilles",
				"desc_en": "",
				"name_ru": "ÐÐ¸Ð´ÐµÑ€Ð»Ð°Ð½Ð´ÑÐºÐ¸Ðµ ÐÐ½Ñ‚Ð¸Ð»ÑŒÑÐºÐ¸Ðµ Ð¾ÑÑ‚Ñ€Ð¾Ð²Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+599-9###-####",
				"cc": "AN",
				"cd": "Netherlands Antilles",
				"desc_en": "Curacao",
				"name_ru": "ÐÐ¸Ð´ÐµÑ€Ð»Ð°Ð½Ð´ÑÐºÐ¸Ðµ ÐÐ½Ñ‚Ð¸Ð»ÑŒÑÐºÐ¸Ðµ Ð¾ÑÑ‚Ñ€Ð¾Ð²Ð°",
				"desc_ru": "ÐšÑŽÑ€Ð°ÑÐ°Ð¾"
			},
			{
				"mask": "+244(###)###-###",
				"cc": "AO",
				"cd": "Angola",
				"desc_en": "",
				"name_ru": "ÐÐ½Ð³Ð¾Ð»Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+672-1##-###",
				"cc": "AQ",
				"cd": "Australian bases in Antarctica",
				"desc_en": "",
				"name_ru": "ÐÐ²ÑÑ‚Ñ€Ð°Ð»Ð¸Ð¹ÑÐºÐ°Ñ Ð°Ð½Ñ‚Ð°Ñ€ÐºÑ‚Ð¸Ñ‡ÐµÑÐºÐ°Ñ Ð±Ð°Ð·Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+54(###)###-####",
				"cc": "AR",
				"cd": "Argentina",
				"desc_en": "",
				"name_ru": "ÐÑ€Ð³ÐµÐ½Ñ‚Ð¸Ð½Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+1(684)###-####",
				"cc": "AS",
				"cd": "American Samoa",
				"desc_en": "",
				"name_ru": "ÐÐ¼ÐµÑ€Ð¸ÐºÐ°Ð½ÑÐºÐ¾Ðµ Ð¡Ð°Ð¼Ð¾Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+43(###)###-####",
				"cc": "AT",
				"cd": "Austria",
				"desc_en": "",
				"name_ru": "ÐÐ²ÑÑ‚Ñ€Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+61-#-####-####",
				"cc": "AU",
				"cd": "Australia",
				"desc_en": "",
				"name_ru": "ÐÐ²ÑÑ‚Ñ€Ð°Ð»Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+297-###-####",
				"cc": "AW",
				"cd": "Aruba",
				"desc_en": "",
				"name_ru": "ÐÑ€ÑƒÐ±Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+994-##-###-##-##",
				"cc": "AZ",
				"cd": "Azerbaijan",
				"desc_en": "",
				"name_ru": "ÐÐ·ÐµÑ€Ð±Ð°Ð¹Ð´Ð¶Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+387-##-#####",
				"cc": "BA",
				"cd": "Bosnia and Herzegovina",
				"desc_en": "",
				"name_ru": "Ð‘Ð¾ÑÐ½Ð¸Ñ Ð¸ Ð“ÐµÑ€Ñ†ÐµÐ³Ð¾Ð²Ð¸Ð½Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+387-##-####",
				"cc": "BA",
				"cd": "Bosnia and Herzegovina",
				"desc_en": "",
				"name_ru": "Ð‘Ð¾ÑÐ½Ð¸Ñ Ð¸ Ð“ÐµÑ€Ñ†ÐµÐ³Ð¾Ð²Ð¸Ð½Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+1(246)###-####",
				"cc": "BB",
				"cd": "Barbados",
				"desc_en": "",
				"name_ru": "Ð‘Ð°Ñ€Ð±Ð°Ð´Ð¾Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+880-##-###-###",
				"cc": "BD",
				"cd": "Bangladesh",
				"desc_en": "",
				"name_ru": "Ð‘Ð°Ð½Ð³Ð»Ð°Ð´ÐµÑˆ",
				"desc_ru": ""
			},
			{
				"mask": "+32(###)###-###",
				"cc": "BE",
				"cd": "Belgium",
				"desc_en": "",
				"name_ru": "Ð‘ÐµÐ»ÑŒÐ³Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+226-##-##-####",
				"cc": "BF",
				"cd": "Burkina Faso",
				"desc_en": "",
				"name_ru": "Ð‘ÑƒÑ€ÐºÐ¸Ð½Ð° Ð¤Ð°ÑÐ¾",
				"desc_ru": ""
			},
			{
				"mask": "+359(###)###-###",
				"cc": "BG",
				"cd": "Bulgaria",
				"desc_en": "",
				"name_ru": "Ð‘Ð¾Ð»Ð³Ð°Ñ€Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+973-####-####",
				"cc": "BH",
				"cd": "Bahrain",
				"desc_en": "",
				"name_ru": "Ð‘Ð°Ñ…Ñ€ÐµÐ¹Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+257-##-##-####",
				"cc": "BI",
				"cd": "Burundi",
				"desc_en": "",
				"name_ru": "Ð‘ÑƒÑ€ÑƒÐ½Ð´Ð¸",
				"desc_ru": ""
			},
			{
				"mask": "+229-##-##-####",
				"cc": "BJ",
				"cd": "Benin",
				"desc_en": "",
				"name_ru": "Ð‘ÐµÐ½Ð¸Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+1(441)###-####",
				"cc": "BM",
				"cd": "Bermuda",
				"desc_en": "",
				"name_ru": "Ð‘ÐµÑ€Ð¼ÑƒÐ´ÑÐºÐ¸Ðµ Ð¾ÑÑ‚Ñ€Ð¾Ð²Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+673-###-####",
				"cc": "BN",
				"cd": "Brunei Darussalam",
				"desc_en": "",
				"name_ru": "Ð‘Ñ€ÑƒÐ½ÐµÐ¹-Ð”Ð°Ñ€ÑƒÑÑÐ°Ð»Ð°Ð¼",
				"desc_ru": ""
			},
			{
				"mask": "+591-#-###-####",
				"cc": "BO",
				"cd": "Bolivia",
				"desc_en": "",
				"name_ru": "Ð‘Ð¾Ð»Ð¸Ð²Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+55-##-####-####",
				"cc": "BR",
				"cd": "Brazil",
				"desc_en": "",
				"name_ru": "Ð‘Ñ€Ð°Ð·Ð¸Ð»Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+55-##-#####-####",
				"cc": "BR",
				"cd": "Brazil",
				"desc_en": "",
				"name_ru": "Ð‘Ñ€Ð°Ð·Ð¸Ð»Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+1(242)###-####",
				"cc": "BS",
				"cd": "Bahamas",
				"desc_en": "",
				"name_ru": "Ð‘Ð°Ð³Ð°Ð¼ÑÐºÐ¸Ðµ ÐžÑÑ‚Ñ€Ð¾Ð²Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+975-17-###-###",
				"cc": "BT",
				"cd": "Bhutan",
				"desc_en": "",
				"name_ru": "Ð‘ÑƒÑ‚Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+975-#-###-###",
				"cc": "BT",
				"cd": "Bhutan",
				"desc_en": "",
				"name_ru": "Ð‘ÑƒÑ‚Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+267-##-###-###",
				"cc": "BW",
				"cd": "Botswana",
				"desc_en": "",
				"name_ru": "Ð‘Ð¾Ñ‚ÑÐ²Ð°Ð½Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+375(##)###-##-##",
				"cc": "BY",
				"cd": "Belarus",
				"desc_en": "",
				"name_ru": "Ð‘ÐµÐ»Ð°Ñ€ÑƒÑÑŒ (Ð‘ÐµÐ»Ð¾Ñ€ÑƒÑÑÐ¸Ñ)",
				"desc_ru": ""
			},
			{
				"mask": "+501-###-####",
				"cc": "BZ",
				"cd": "Belize",
				"desc_en": "",
				"name_ru": "Ð‘ÐµÐ»Ð¸Ð·",
				"desc_ru": ""
			},
			{
				"mask": "+243(###)###-###",
				"cc": "CD",
				"cd": "Dem. Rep. Congo",
				"desc_en": "",
				"name_ru": "Ð”ÐµÐ¼. Ð ÐµÑÐ¿. ÐšÐ¾Ð½Ð³Ð¾ (ÐšÐ¸Ð½ÑˆÐ°ÑÐ°)",
				"desc_ru": ""
			},
			{
				"mask": "+236-##-##-####",
				"cc": "CF",
				"cd": "Central African Republic",
				"desc_en": "",
				"name_ru": "Ð¦ÐµÐ½Ñ‚Ñ€Ð°Ð»ÑŒÐ½Ð¾Ð°Ñ„Ñ€Ð¸ÐºÐ°Ð½ÑÐºÐ°Ñ Ð ÐµÑÐ¿ÑƒÐ±Ð»Ð¸ÐºÐ°",
				"desc_ru": ""
			},
			{
				"mask": "+242-##-###-####",
				"cc": "CG",
				"cd": "Congo (Brazzaville)",
				"desc_en": "",
				"name_ru": "ÐšÐ¾Ð½Ð³Ð¾ (Ð‘Ñ€Ð°Ð·Ð·Ð°Ð²Ð¸Ð»ÑŒ)",
				"desc_ru": ""
			},
			{
				"mask": "+41-##-###-####",
				"cc": "CH",
				"cd": "Switzerland",
				"desc_en": "",
				"name_ru": "Ð¨Ð²ÐµÐ¹Ñ†Ð°Ñ€Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+225-##-###-###",
				"cc": "CI",
				"cd": "Cote dâ€™Ivoire (Ivory Coast)",
				"desc_en": "",
				"name_ru": "ÐšÐ¾Ñ‚-Ð´â€™Ð˜Ð²ÑƒÐ°Ñ€",
				"desc_ru": ""
			},
			{
				"mask": "+682-##-###",
				"cc": "CK",
				"cd": "Cook Islands",
				"desc_en": "",
				"name_ru": "ÐžÑÑ‚Ñ€Ð¾Ð²Ð° ÐšÑƒÐºÐ°",
				"desc_ru": ""
			},
			{
				"mask": "+56-#-####-####",
				"cc": "CL",
				"cd": "Chile",
				"desc_en": "",
				"name_ru": "Ð§Ð¸Ð»Ð¸",
				"desc_ru": ""
			},
			{
				"mask": "+237-####-####",
				"cc": "CM",
				"cd": "Cameroon",
				"desc_en": "",
				"name_ru": "ÐšÐ°Ð¼ÐµÑ€ÑƒÐ½",
				"desc_ru": ""
			},
			{
				"mask": "+86(###)####-####",
				"cc": "CN",
				"cd": "China (PRC)",
				"desc_en": "",
				"name_ru": "ÐšÐ¸Ñ‚Ð°Ð¹ÑÐºÐ°Ñ Ð.Ð .",
				"desc_ru": ""
			},
			{
				"mask": "+86(###)####-###",
				"cc": "CN",
				"cd": "China (PRC)",
				"desc_en": "",
				"name_ru": "ÐšÐ¸Ñ‚Ð°Ð¹ÑÐºÐ°Ñ Ð.Ð .",
				"desc_ru": ""
			},
			{
				"mask": "+86-##-#####-#####",
				"cc": "CN",
				"cd": "China (PRC)",
				"desc_en": "",
				"name_ru": "ÐšÐ¸Ñ‚Ð°Ð¹ÑÐºÐ°Ñ Ð.Ð .",
				"desc_ru": ""
			},
			{
				"mask": "+57(###)###-####",
				"cc": "CO",
				"cd": "Colombia",
				"desc_en": "",
				"name_ru": "ÐšÐ¾Ð»ÑƒÐ¼Ð±Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+506-####-####",
				"cc": "CR",
				"cd": "Costa Rica",
				"desc_en": "",
				"name_ru": "ÐšÐ¾ÑÑ‚Ð°-Ð Ð¸ÐºÐ°",
				"desc_ru": ""
			},
			{
				"mask": "+53-#-###-####",
				"cc": "CU",
				"cd": "Cuba",
				"desc_en": "",
				"name_ru": "ÐšÑƒÐ±Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+238(###)##-##",
				"cc": "CV",
				"cd": "Cape Verde",
				"desc_en": "",
				"name_ru": "ÐšÐ°Ð±Ð¾-Ð’ÐµÑ€Ð´Ðµ",
				"desc_ru": ""
			},
			{
				"mask": "+599-###-####",
				"cc": "CW",
				"cd": "Curacao",
				"desc_en": "",
				"name_ru": "ÐšÑŽÑ€Ð°ÑÐ°Ð¾",
				"desc_ru": ""
			},
			{
				"mask": "+357-##-###-###",
				"cc": "CY",
				"cd": "Cyprus",
				"desc_en": "",
				"name_ru": "ÐšÐ¸Ð¿Ñ€",
				"desc_ru": ""
			},
			{
				"mask": "+420(###)###-###",
				"cc": "CZ",
				"cd": "Czech Republic",
				"desc_en": "",
				"name_ru": "Ð§ÐµÑ…Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+49(####)###-####",
				"cc": "DE",
				"cd": "Germany",
				"desc_en": "",
				"name_ru": "Ð“ÐµÑ€Ð¼Ð°Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+49(###)###-####",
				"cc": "DE",
				"cd": "Germany",
				"desc_en": "",
				"name_ru": "Ð“ÐµÑ€Ð¼Ð°Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+49(###)##-####",
				"cc": "DE",
				"cd": "Germany",
				"desc_en": "",
				"name_ru": "Ð“ÐµÑ€Ð¼Ð°Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+49(###)##-###",
				"cc": "DE",
				"cd": "Germany",
				"desc_en": "",
				"name_ru": "Ð“ÐµÑ€Ð¼Ð°Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+49(###)##-##",
				"cc": "DE",
				"cd": "Germany",
				"desc_en": "",
				"name_ru": "Ð“ÐµÑ€Ð¼Ð°Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+49-###-###",
				"cc": "DE",
				"cd": "Germany",
				"desc_en": "",
				"name_ru": "Ð“ÐµÑ€Ð¼Ð°Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+253-##-##-##-##",
				"cc": "DJ",
				"cd": "Djibouti",
				"desc_en": "",
				"name_ru": "Ð”Ð¶Ð¸Ð±ÑƒÑ‚Ð¸",
				"desc_ru": ""
			},
			{
				"mask": "+45-##-##-##-##",
				"cc": "DK",
				"cd": "Denmark",
				"desc_en": "",
				"name_ru": "Ð”Ð°Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+1(767)###-####",
				"cc": "DM",
				"cd": "Dominica",
				"desc_en": "",
				"name_ru": "Ð”Ð¾Ð¼Ð¸Ð½Ð¸ÐºÐ°",
				"desc_ru": ""
			},
			{
				"mask": "+1(809)###-####",
				"cc": "DO",
				"cd": "Dominican Republic",
				"desc_en": "",
				"name_ru": "Ð”Ð¾Ð¼Ð¸Ð½Ð¸ÐºÐ°Ð½ÑÐºÐ°Ñ Ð ÐµÑÐ¿ÑƒÐ±Ð»Ð¸ÐºÐ°",
				"desc_ru": ""
			},
			{
				"mask": "+1(829)###-####",
				"cc": "DO",
				"cd": "Dominican Republic",
				"desc_en": "",
				"name_ru": "Ð”Ð¾Ð¼Ð¸Ð½Ð¸ÐºÐ°Ð½ÑÐºÐ°Ñ Ð ÐµÑÐ¿ÑƒÐ±Ð»Ð¸ÐºÐ°",
				"desc_ru": ""
			},
			{
				"mask": "+1(849)###-####",
				"cc": "DO",
				"cd": "Dominican Republic",
				"desc_en": "",
				"name_ru": "Ð”Ð¾Ð¼Ð¸Ð½Ð¸ÐºÐ°Ð½ÑÐºÐ°Ñ Ð ÐµÑÐ¿ÑƒÐ±Ð»Ð¸ÐºÐ°",
				"desc_ru": ""
			},
			{
				"mask": "+213-##-###-####",
				"cc": "DZ",
				"cd": "Algeria",
				"desc_en": "",
				"name_ru": "ÐÐ»Ð¶Ð¸Ñ€",
				"desc_ru": ""
			},
			{
				"mask": "+593-##-###-####",
				"cc": "EC",
				"cd": "Ecuador ",
				"desc_en": "mobile",
				"name_ru": "Ð­ÐºÐ²Ð°Ð´Ð¾Ñ€ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+593-#-###-####",
				"cc": "EC",
				"cd": "Ecuador",
				"desc_en": "",
				"name_ru": "Ð­ÐºÐ²Ð°Ð´Ð¾Ñ€",
				"desc_ru": ""
			},
			{
				"mask": "+372-####-####",
				"cc": "EE",
				"cd": "Estonia ",
				"desc_en": "mobile",
				"name_ru": "Ð­ÑÑ‚Ð¾Ð½Ð¸Ñ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+372-###-####",
				"cc": "EE",
				"cd": "Estonia",
				"desc_en": "",
				"name_ru": "Ð­ÑÑ‚Ð¾Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+20(###)###-####",
				"cc": "EG",
				"cd": "Egypt",
				"desc_en": "",
				"name_ru": "Ð•Ð³Ð¸Ð¿ÐµÑ‚",
				"desc_ru": ""
			},
			{
				"mask": "+291-#-###-###",
				"cc": "ER",
				"cd": "Eritrea",
				"desc_en": "",
				"name_ru": "Ð­Ñ€Ð¸Ñ‚Ñ€ÐµÑ",
				"desc_ru": ""
			},
			{
				"mask": "+34(###)###-###",
				"cc": "ES",
				"cd": "Spain",
				"desc_en": "",
				"name_ru": "Ð˜ÑÐ¿Ð°Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+251-##-###-####",
				"cc": "ET",
				"cd": "Ethiopia",
				"desc_en": "",
				"name_ru": "Ð­Ñ„Ð¸Ð¾Ð¿Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+358(###)###-##-##",
				"cc": "FI",
				"cd": "Finland",
				"desc_en": "",
				"name_ru": "Ð¤Ð¸Ð½Ð»ÑÐ½Ð´Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+679-##-#####",
				"cc": "FJ",
				"cd": "Fiji",
				"desc_en": "",
				"name_ru": "Ð¤Ð¸Ð´Ð¶Ð¸",
				"desc_ru": ""
			},
			{
				"mask": "+500-#####",
				"cc": "FK",
				"cd": "Falkland Islands",
				"desc_en": "",
				"name_ru": "Ð¤Ð¾Ð»ÐºÐ»ÐµÐ½Ð´ÑÐºÐ¸Ðµ Ð¾ÑÑ‚Ñ€Ð¾Ð²Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+691-###-####",
				"cc": "FM",
				"cd": "F.S. Micronesia",
				"desc_en": "",
				"name_ru": "Ð¤.Ð¨. ÐœÐ¸ÐºÑ€Ð¾Ð½ÐµÐ·Ð¸Ð¸",
				"desc_ru": ""
			},
			{
				"mask": "+298-###-###",
				"cc": "FO",
				"cd": "Faroe Islands",
				"desc_en": "",
				"name_ru": "Ð¤Ð°Ñ€ÐµÑ€ÑÐºÐ¸Ðµ Ð¾ÑÑ‚Ñ€Ð¾Ð²Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+262-#####-####",
				"cc": "FR",
				"cd": "Mayotte",
				"desc_en": "",
				"name_ru": "ÐœÐ°Ð¹Ð¾Ñ‚Ñ‚Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+33(###)###-###",
				"cc": "FR",
				"cd": "France",
				"desc_en": "",
				"name_ru": "Ð¤Ñ€Ð°Ð½Ñ†Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+508-##-####",
				"cc": "FR",
				"cd": "St Pierre & Miquelon",
				"desc_en": "",
				"name_ru": "Ð¡ÐµÐ½-ÐŸÑŒÐµÑ€ Ð¸ ÐœÐ¸ÐºÐµÐ»Ð¾Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+590(###)###-###",
				"cc": "FR",
				"cd": "Guadeloupe",
				"desc_en": "",
				"name_ru": "Ð“Ð²Ð°Ð´ÐµÐ»ÑƒÐ¿Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+241-#-##-##-##",
				"cc": "GA",
				"cd": "Gabon",
				"desc_en": "",
				"name_ru": "Ð“Ð°Ð±Ð¾Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+1(473)###-####",
				"cc": "GD",
				"cd": "Grenada",
				"desc_en": "",
				"name_ru": "Ð“Ñ€ÐµÐ½Ð°Ð´Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+995(###)###-###",
				"cc": "GE",
				"cd": "Rep. of Georgia",
				"desc_en": "",
				"name_ru": "Ð“Ñ€ÑƒÐ·Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+594-#####-####",
				"cc": "GF",
				"cd": "Guiana (French)",
				"desc_en": "",
				"name_ru": "Ð¤Ñ€. Ð“Ð²Ð¸Ð°Ð½Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+233(###)###-###",
				"cc": "GH",
				"cd": "Ghana",
				"desc_en": "",
				"name_ru": "Ð“Ð°Ð½Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+350-###-#####",
				"cc": "GI",
				"cd": "Gibraltar",
				"desc_en": "",
				"name_ru": "Ð“Ð¸Ð±Ñ€Ð°Ð»Ñ‚Ð°Ñ€",
				"desc_ru": ""
			},
			{
				"mask": "+299-##-##-##",
				"cc": "GL",
				"cd": "Greenland",
				"desc_en": "",
				"name_ru": "Ð“Ñ€ÐµÐ½Ð»Ð°Ð½Ð´Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+220(###)##-##",
				"cc": "GM",
				"cd": "Gambia",
				"desc_en": "",
				"name_ru": "Ð“Ð°Ð¼Ð±Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+224-##-###-###",
				"cc": "GN",
				"cd": "Guinea",
				"desc_en": "",
				"name_ru": "Ð“Ð²Ð¸Ð½ÐµÑ",
				"desc_ru": ""
			},
			{
				"mask": "+240-##-###-####",
				"cc": "GQ",
				"cd": "Equatorial Guinea",
				"desc_en": "",
				"name_ru": "Ð­ÐºÐ²Ð°Ñ‚Ð¾Ñ€Ð¸Ð°Ð»ÑŒÐ½Ð°Ñ Ð“Ð²Ð¸Ð½ÐµÑ",
				"desc_ru": ""
			},
			{
				"mask": "+30(###)###-####",
				"cc": "GR",
				"cd": "Greece",
				"desc_en": "",
				"name_ru": "Ð“Ñ€ÐµÑ†Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+502-#-###-####",
				"cc": "GT",
				"cd": "Guatemala",
				"desc_en": "",
				"name_ru": "Ð“Ð²Ð°Ñ‚ÐµÐ¼Ð°Ð»Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+1(671)###-####",
				"cc": "GU",
				"cd": "Guam",
				"desc_en": "",
				"name_ru": "Ð“ÑƒÐ°Ð¼",
				"desc_ru": ""
			},
			{
				"mask": "+245-#-######",
				"cc": "GW",
				"cd": "Guinea-Bissau",
				"desc_en": "",
				"name_ru": "Ð“Ð²Ð¸Ð½ÐµÑ-Ð‘Ð¸ÑÐ°Ñƒ",
				"desc_ru": ""
			},
			{
				"mask": "+592-###-####",
				"cc": "GY",
				"cd": "Guyana",
				"desc_en": "",
				"name_ru": "Ð“Ð°Ð¹Ð°Ð½Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+852-####-####",
				"cc": "HK",
				"cd": "Hong Kong",
				"desc_en": "",
				"name_ru": "Ð“Ð¾Ð½ÐºÐ¾Ð½Ð³",
				"desc_ru": ""
			},
			{
				"mask": "+504-####-####",
				"cc": "HN",
				"cd": "Honduras",
				"desc_en": "",
				"name_ru": "Ð“Ð¾Ð½Ð´ÑƒÑ€Ð°Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+385-##-###-###",
				"cc": "HR",
				"cd": "Croatia",
				"desc_en": "",
				"name_ru": "Ð¥Ð¾Ñ€Ð²Ð°Ñ‚Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+385-1-###-###",
				"cc": "HR",
				"cd": "Croatia",
				"desc_en": "",
				"name_ru": "Ð¥Ð¾Ñ€Ð²Ð°Ñ‚Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+509-##-##-####",
				"cc": "HT",
				"cd": "Haiti",
				"desc_en": "",
				"name_ru": "Ð“Ð°Ð¸Ñ‚Ð¸",
				"desc_ru": ""
			},
			{
				"mask": "+36(###)###-###",
				"cc": "HU",
				"cd": "Hungary",
				"desc_en": "",
				"name_ru": "Ð’ÐµÐ½Ð³Ñ€Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+62(8##)###-####",
				"cc": "ID",
				"cd": "Indonesia ",
				"desc_en": "mobile",
				"name_ru": "Ð˜Ð½Ð´Ð¾Ð½ÐµÐ·Ð¸Ñ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+62-##-###-##",
				"cc": "ID",
				"cd": "Indonesia",
				"desc_en": "",
				"name_ru": "Ð˜Ð½Ð´Ð¾Ð½ÐµÐ·Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+62-##-###-###",
				"cc": "ID",
				"cd": "Indonesia",
				"desc_en": "",
				"name_ru": "Ð˜Ð½Ð´Ð¾Ð½ÐµÐ·Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+62-##-###-####",
				"cc": "ID",
				"cd": "Indonesia",
				"desc_en": "",
				"name_ru": "Ð˜Ð½Ð´Ð¾Ð½ÐµÐ·Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+62(8##)###-###",
				"cc": "ID",
				"cd": "Indonesia ",
				"desc_en": "mobile",
				"name_ru": "Ð˜Ð½Ð´Ð¾Ð½ÐµÐ·Ð¸Ñ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+62(8##)###-##-###",
				"cc": "ID",
				"cd": "Indonesia ",
				"desc_en": "mobile",
				"name_ru": "Ð˜Ð½Ð´Ð¾Ð½ÐµÐ·Ð¸Ñ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+353(###)###-###",
				"cc": "IE",
				"cd": "Ireland",
				"desc_en": "",
				"name_ru": "Ð˜Ñ€Ð»Ð°Ð½Ð´Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+972-5#-###-####",
				"cc": "IL",
				"cd": "Israel ",
				"desc_en": "mobile",
				"name_ru": "Ð˜Ð·Ñ€Ð°Ð¸Ð»ÑŒ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+972-#-###-####",
				"cc": "IL",
				"cd": "Israel",
				"desc_en": "",
				"name_ru": "Ð˜Ð·Ñ€Ð°Ð¸Ð»ÑŒ",
				"desc_ru": ""
			},
			{
				"mask": "+91(####)###-###",
				"cc": "IN",
				"cd": "India",
				"desc_en": "",
				"name_ru": "Ð˜Ð½Ð´Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+246-###-####",
				"cc": "IO",
				"cd": "Diego Garcia",
				"desc_en": "",
				"name_ru": "Ð”Ð¸ÐµÐ³Ð¾-Ð“Ð°Ñ€ÑÐ¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+964(###)###-####",
				"cc": "IQ",
				"cd": "Iraq",
				"desc_en": "",
				"name_ru": "Ð˜Ñ€Ð°Ðº",
				"desc_ru": ""
			},
			{
				"mask": "+98(###)###-####",
				"cc": "IR",
				"cd": "Iran",
				"desc_en": "",
				"name_ru": "Ð˜Ñ€Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+354-###-####",
				"cc": "IS",
				"cd": "Iceland",
				"desc_en": "",
				"name_ru": "Ð˜ÑÐ»Ð°Ð½Ð´Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+39(###)####-###",
				"cc": "IT",
				"cd": "Italy",
				"desc_en": "",
				"name_ru": "Ð˜Ñ‚Ð°Ð»Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+1(876)###-####",
				"cc": "JM",
				"cd": "Jamaica",
				"desc_en": "",
				"name_ru": "Ð¯Ð¼Ð°Ð¹ÐºÐ°",
				"desc_ru": ""
			},
			{
				"mask": "+962-#-####-####",
				"cc": "JO",
				"cd": "Jordan",
				"desc_en": "",
				"name_ru": "Ð˜Ð¾Ñ€Ð´Ð°Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+81-##-####-####",
				"cc": "JP",
				"cd": "Japan ",
				"desc_en": "mobile",
				"name_ru": "Ð¯Ð¿Ð¾Ð½Ð¸Ñ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+81(###)###-###",
				"cc": "JP",
				"cd": "Japan",
				"desc_en": "",
				"name_ru": "Ð¯Ð¿Ð¾Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+254-###-######",
				"cc": "KE",
				"cd": "Kenya",
				"desc_en": "",
				"name_ru": "ÐšÐµÐ½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+996(###)###-###",
				"cc": "KG",
				"cd": "Kyrgyzstan",
				"desc_en": "",
				"name_ru": "ÐšÐ¸Ñ€Ð³Ð¸Ð·Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+855-##-###-###",
				"cc": "KH",
				"cd": "Cambodia",
				"desc_en": "",
				"name_ru": "ÐšÐ°Ð¼Ð±Ð¾Ð´Ð¶Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+686-##-###",
				"cc": "KI",
				"cd": "Kiribati",
				"desc_en": "",
				"name_ru": "ÐšÐ¸Ñ€Ð¸Ð±Ð°Ñ‚Ð¸",
				"desc_ru": ""
			},
			{
				"mask": "+269-##-#####",
				"cc": "KM",
				"cd": "Comoros",
				"desc_en": "",
				"name_ru": "ÐšÐ¾Ð¼Ð¾Ñ€Ñ‹",
				"desc_ru": ""
			},
			{
				"mask": "+1(869)###-####",
				"cc": "KN",
				"cd": "Saint Kitts & Nevis",
				"desc_en": "",
				"name_ru": "Ð¡ÐµÐ½Ñ‚-ÐšÐ¸Ñ‚Ñ Ð¸ ÐÐµÐ²Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+850-191-###-####",
				"cc": "KP",
				"cd": "DPR Korea (North) ",
				"desc_en": "mobile",
				"name_ru": "ÐšÐ¾Ñ€ÐµÐ¹ÑÐºÐ°Ñ ÐÐ”Ð  ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+850-##-###-###",
				"cc": "KP",
				"cd": "DPR Korea (North)",
				"desc_en": "",
				"name_ru": "ÐšÐ¾Ñ€ÐµÐ¹ÑÐºÐ°Ñ ÐÐ”Ð ",
				"desc_ru": ""
			},
			{
				"mask": "+850-###-####-###",
				"cc": "KP",
				"cd": "DPR Korea (North)",
				"desc_en": "",
				"name_ru": "ÐšÐ¾Ñ€ÐµÐ¹ÑÐºÐ°Ñ ÐÐ”Ð ",
				"desc_ru": ""
			},
			{
				"mask": "+850-###-###",
				"cc": "KP",
				"cd": "DPR Korea (North)",
				"desc_en": "",
				"name_ru": "ÐšÐ¾Ñ€ÐµÐ¹ÑÐºÐ°Ñ ÐÐ”Ð ",
				"desc_ru": ""
			},
			{
				"mask": "+850-####-####",
				"cc": "KP",
				"cd": "DPR Korea (North)",
				"desc_en": "",
				"name_ru": "ÐšÐ¾Ñ€ÐµÐ¹ÑÐºÐ°Ñ ÐÐ”Ð ",
				"desc_ru": ""
			},
			{
				"mask": "+850-####-#############",
				"cc": "KP",
				"cd": "DPR Korea (North)",
				"desc_en": "",
				"name_ru": "ÐšÐ¾Ñ€ÐµÐ¹ÑÐºÐ°Ñ ÐÐ”Ð ",
				"desc_ru": ""
			},
			{
				"mask": "+82-##-###-####",
				"cc": "KR",
				"cd": "Korea (South)",
				"desc_en": "",
				"name_ru": "Ð ÐµÑÐ¿. ÐšÐ¾Ñ€ÐµÑ",
				"desc_ru": ""
			},
			{
				"mask": "+965-####-####",
				"cc": "KW",
				"cd": "Kuwait",
				"desc_en": "",
				"name_ru": "ÐšÑƒÐ²ÐµÐ¹Ñ‚",
				"desc_ru": ""
			},
			{
				"mask": "+1(345)###-####",
				"cc": "KY",
				"cd": "Cayman Islands",
				"desc_en": "",
				"name_ru": "ÐšÐ°Ð¹Ð¼Ð°Ð½Ð¾Ð²Ñ‹ Ð¾ÑÑ‚Ñ€Ð¾Ð²Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+7(6##)###-##-##",
				"cc": "KZ",
				"cd": "Kazakhstan",
				"desc_en": "",
				"name_ru": "ÐšÐ°Ð·Ð°Ñ…ÑÑ‚Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+7(7##)###-##-##",
				"cc": "KZ",
				"cd": "Kazakhstan",
				"desc_en": "",
				"name_ru": "ÐšÐ°Ð·Ð°Ñ…ÑÑ‚Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+856(20##)###-###",
				"cc": "LA",
				"cd": "Laos ",
				"desc_en": "mobile",
				"name_ru": "Ð›Ð°Ð¾Ñ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+856-##-###-###",
				"cc": "LA",
				"cd": "Laos",
				"desc_en": "",
				"name_ru": "Ð›Ð°Ð¾Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+961-##-###-###",
				"cc": "LB",
				"cd": "Lebanon ",
				"desc_en": "mobile",
				"name_ru": "Ð›Ð¸Ð²Ð°Ð½ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+961-#-###-###",
				"cc": "LB",
				"cd": "Lebanon",
				"desc_en": "",
				"name_ru": "Ð›Ð¸Ð²Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+1(758)###-####",
				"cc": "LC",
				"cd": "Saint Lucia",
				"desc_en": "",
				"name_ru": "Ð¡ÐµÐ½Ñ‚-Ð›ÑŽÑÐ¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+423(###)###-####",
				"cc": "LI",
				"cd": "Liechtenstein",
				"desc_en": "",
				"name_ru": "Ð›Ð¸Ñ…Ñ‚ÐµÐ½ÑˆÑ‚ÐµÐ¹Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+94-##-###-####",
				"cc": "LK",
				"cd": "Sri Lanka",
				"desc_en": "",
				"name_ru": "Ð¨Ñ€Ð¸-Ð›Ð°Ð½ÐºÐ°",
				"desc_ru": ""
			},
			{
				"mask": "+231-##-###-###",
				"cc": "LR",
				"cd": "Liberia",
				"desc_en": "",
				"name_ru": "Ð›Ð¸Ð±ÐµÑ€Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+266-#-###-####",
				"cc": "LS",
				"cd": "Lesotho",
				"desc_en": "",
				"name_ru": "Ð›ÐµÑÐ¾Ñ‚Ð¾",
				"desc_ru": ""
			},
			{
				"mask": "+370(###)##-###",
				"cc": "LT",
				"cd": "Lithuania",
				"desc_en": "",
				"name_ru": "Ð›Ð¸Ñ‚Ð²Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+352(###)###-###",
				"cc": "LU",
				"cd": "Luxembourg",
				"desc_en": "",
				"name_ru": "Ð›ÑŽÐºÑÐµÐ¼Ð±ÑƒÑ€Ð³",
				"desc_ru": ""
			},
			{
				"mask": "+371-##-###-###",
				"cc": "LV",
				"cd": "Latvia",
				"desc_en": "",
				"name_ru": "Ð›Ð°Ñ‚Ð²Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+218-##-###-###",
				"cc": "LY",
				"cd": "Libya",
				"desc_en": "",
				"name_ru": "Ð›Ð¸Ð²Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+218-21-###-####",
				"cc": "LY",
				"cd": "Libya",
				"desc_en": "Tripoli",
				"name_ru": "Ð›Ð¸Ð²Ð¸Ñ",
				"desc_ru": "Ð¢Ñ€Ð¸Ð¿Ð¾Ð»Ð¸"
			},
			{
				"mask": "+212-##-####-###",
				"cc": "MA",
				"cd": "Morocco",
				"desc_en": "",
				"name_ru": "ÐœÐ°Ñ€Ð¾ÐºÐºÐ¾",
				"desc_ru": ""
			},
			{
				"mask": "+377(###)###-###",
				"cc": "MC",
				"cd": "Monaco",
				"desc_en": "",
				"name_ru": "ÐœÐ¾Ð½Ð°ÐºÐ¾",
				"desc_ru": ""
			},
			{
				"mask": "+377-##-###-###",
				"cc": "MC",
				"cd": "Monaco",
				"desc_en": "",
				"name_ru": "ÐœÐ¾Ð½Ð°ÐºÐ¾",
				"desc_ru": ""
			},
			{
				"mask": "+373-####-####",
				"cc": "MD",
				"cd": "Moldova",
				"desc_en": "",
				"name_ru": "ÐœÐ¾Ð»Ð´Ð¾Ð²Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+382-##-###-###",
				"cc": "ME",
				"cd": "Montenegro",
				"desc_en": "",
				"name_ru": "Ð§ÐµÑ€Ð½Ð¾Ð³Ð¾Ñ€Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+261-##-##-#####",
				"cc": "MG",
				"cd": "Madagascar",
				"desc_en": "",
				"name_ru": "ÐœÐ°Ð´Ð°Ð³Ð°ÑÐºÐ°Ñ€",
				"desc_ru": ""
			},
			{
				"mask": "+692-###-####",
				"cc": "MH",
				"cd": "Marshall Islands",
				"desc_en": "",
				"name_ru": "ÐœÐ°Ñ€ÑˆÐ°Ð»Ð»Ð¾Ð²Ñ‹ ÐžÑÑ‚Ñ€Ð¾Ð²Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+389-##-###-###",
				"cc": "MK",
				"cd": "Republic of Macedonia",
				"desc_en": "",
				"name_ru": "Ð ÐµÑÐ¿. ÐœÐ°ÐºÐµÐ´Ð¾Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+223-##-##-####",
				"cc": "ML",
				"cd": "Mali",
				"desc_en": "",
				"name_ru": "ÐœÐ°Ð»Ð¸",
				"desc_ru": ""
			},
			{
				"mask": "+95-##-###-###",
				"cc": "MM",
				"cd": "Burma (Myanmar)",
				"desc_en": "",
				"name_ru": "Ð‘Ð¸Ñ€Ð¼Ð° (ÐœÑŒÑÐ½Ð¼Ð°)",
				"desc_ru": ""
			},
			{
				"mask": "+95-#-###-###",
				"cc": "MM",
				"cd": "Burma (Myanmar)",
				"desc_en": "",
				"name_ru": "Ð‘Ð¸Ñ€Ð¼Ð° (ÐœÑŒÑÐ½Ð¼Ð°)",
				"desc_ru": ""
			},
			{
				"mask": "+95-###-###",
				"cc": "MM",
				"cd": "Burma (Myanmar)",
				"desc_en": "",
				"name_ru": "Ð‘Ð¸Ñ€Ð¼Ð° (ÐœÑŒÑÐ½Ð¼Ð°)",
				"desc_ru": ""
			},
			{
				"mask": "+976-##-##-####",
				"cc": "MN",
				"cd": "Mongolia",
				"desc_en": "",
				"name_ru": "ÐœÐ¾Ð½Ð³Ð¾Ð»Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+853-####-####",
				"cc": "MO",
				"cd": "Macau",
				"desc_en": "",
				"name_ru": "ÐœÐ°ÐºÐ°Ð¾",
				"desc_ru": ""
			},
			{
				"mask": "+1(670)###-####",
				"cc": "MP",
				"cd": "Northern Mariana Islands",
				"desc_en": "",
				"name_ru": "Ð¡ÐµÐ²ÐµÑ€Ð½Ñ‹Ðµ ÐœÐ°Ñ€Ð¸Ð°Ð½ÑÐºÐ¸Ðµ Ð¾ÑÑ‚Ñ€Ð¾Ð²Ð° Ð¡Ð°Ð¹Ð¿Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+596(###)##-##-##",
				"cc": "MQ",
				"cd": "Martinique",
				"desc_en": "",
				"name_ru": "ÐœÐ°Ñ€Ñ‚Ð¸Ð½Ð¸ÐºÐ°",
				"desc_ru": ""
			},
			{
				"mask": "+222-##-##-####",
				"cc": "MR",
				"cd": "Mauritania",
				"desc_en": "",
				"name_ru": "ÐœÐ°Ð²Ñ€Ð¸Ñ‚Ð°Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+1(664)###-####",
				"cc": "MS",
				"cd": "Montserrat",
				"desc_en": "",
				"name_ru": "ÐœÐ¾Ð½Ñ‚ÑÐµÑ€Ñ€Ð°Ñ‚",
				"desc_ru": ""
			},
			{
				"mask": "+356-####-####",
				"cc": "MT",
				"cd": "Malta",
				"desc_en": "",
				"name_ru": "ÐœÐ°Ð»ÑŒÑ‚Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+230-###-####",
				"cc": "MU",
				"cd": "Mauritius",
				"desc_en": "",
				"name_ru": "ÐœÐ°Ð²Ñ€Ð¸ÐºÐ¸Ð¹",
				"desc_ru": ""
			},
			{
				"mask": "+960-###-####",
				"cc": "MV",
				"cd": "Maldives",
				"desc_en": "",
				"name_ru": "ÐœÐ°Ð»ÑŒÐ´Ð¸Ð²ÑÐºÐ¸Ðµ Ð¾ÑÑ‚Ñ€Ð¾Ð²Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+265-1-###-###",
				"cc": "MW",
				"cd": "Malawi",
				"desc_en": "Telecom Ltd",
				"name_ru": "ÐœÐ°Ð»Ð°Ð²Ð¸",
				"desc_ru": "Telecom Ltd"
			},
			{
				"mask": "+265-#-####-####",
				"cc": "MW",
				"cd": "Malawi",
				"desc_en": "",
				"name_ru": "ÐœÐ°Ð»Ð°Ð²Ð¸",
				"desc_ru": ""
			},
			{
				"mask": "+52(###)###-####",
				"cc": "MX",
				"cd": "Mexico",
				"desc_en": "",
				"name_ru": "ÐœÐµÐºÑÐ¸ÐºÐ°",
				"desc_ru": ""
			},
			{
				"mask": "+52-##-##-####",
				"cc": "MX",
				"cd": "Mexico",
				"desc_en": "",
				"name_ru": "ÐœÐµÐºÑÐ¸ÐºÐ°",
				"desc_ru": ""
			},
			{
				"mask": "+60-##-###-####",
				"cc": "MY",
				"cd": "Malaysia ",
				"desc_en": "mobile",
				"name_ru": "ÐœÐ°Ð»Ð°Ð¹Ð·Ð¸Ñ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+60(###)###-###",
				"cc": "MY",
				"cd": "Malaysia",
				"desc_en": "",
				"name_ru": "ÐœÐ°Ð»Ð°Ð¹Ð·Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+60-##-###-###",
				"cc": "MY",
				"cd": "Malaysia",
				"desc_en": "",
				"name_ru": "ÐœÐ°Ð»Ð°Ð¹Ð·Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+60-#-###-###",
				"cc": "MY",
				"cd": "Malaysia",
				"desc_en": "",
				"name_ru": "ÐœÐ°Ð»Ð°Ð¹Ð·Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+258-##-###-###",
				"cc": "MZ",
				"cd": "Mozambique",
				"desc_en": "",
				"name_ru": "ÐœÐ¾Ð·Ð°Ð¼Ð±Ð¸Ðº",
				"desc_ru": ""
			},
			{
				"mask": "+264-##-###-####",
				"cc": "NA",
				"cd": "Namibia",
				"desc_en": "",
				"name_ru": "ÐÐ°Ð¼Ð¸Ð±Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+687-##-####",
				"cc": "NC",
				"cd": "New Caledonia",
				"desc_en": "",
				"name_ru": "ÐÐ¾Ð²Ð°Ñ ÐšÐ°Ð»ÐµÐ´Ð¾Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+227-##-##-####",
				"cc": "NE",
				"cd": "Niger",
				"desc_en": "",
				"name_ru": "ÐÐ¸Ð³ÐµÑ€",
				"desc_ru": ""
			},
			{
				"mask": "+672-3##-###",
				"cc": "NF",
				"cd": "Norfolk Island",
				"desc_en": "",
				"name_ru": "ÐÐ¾Ñ€Ñ„Ð¾Ð»Ðº (Ð¾ÑÑ‚Ñ€Ð¾Ð²)",
				"desc_ru": ""
			},
			{
				"mask": "+234(###)###-####",
				"cc": "NG",
				"cd": "Nigeria",
				"desc_en": "",
				"name_ru": "ÐÐ¸Ð³ÐµÑ€Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+234-##-###-###",
				"cc": "NG",
				"cd": "Nigeria",
				"desc_en": "",
				"name_ru": "ÐÐ¸Ð³ÐµÑ€Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+234-##-###-##",
				"cc": "NG",
				"cd": "Nigeria",
				"desc_en": "",
				"name_ru": "ÐÐ¸Ð³ÐµÑ€Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+234(###)###-####",
				"cc": "NG",
				"cd": "Nigeria ",
				"desc_en": "mobile",
				"name_ru": "ÐÐ¸Ð³ÐµÑ€Ð¸Ñ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+505-####-####",
				"cc": "NI",
				"cd": "Nicaragua",
				"desc_en": "",
				"name_ru": "ÐÐ¸ÐºÐ°Ñ€Ð°Ð³ÑƒÐ°",
				"desc_ru": ""
			},
			{
				"mask": "+31-##-###-####",
				"cc": "NL",
				"cd": "Netherlands",
				"desc_en": "",
				"name_ru": "ÐÐ¸Ð´ÐµÑ€Ð»Ð°Ð½Ð´Ñ‹",
				"desc_ru": ""
			},
			{
				"mask": "+47(###)##-###",
				"cc": "NO",
				"cd": "Norway",
				"desc_en": "",
				"name_ru": "ÐÐ¾Ñ€Ð²ÐµÐ³Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+977-##-###-###",
				"cc": "NP",
				"cd": "Nepal",
				"desc_en": "",
				"name_ru": "ÐÐµÐ¿Ð°Ð»",
				"desc_ru": ""
			},
			{
				"mask": "+674-###-####",
				"cc": "NR",
				"cd": "Nauru",
				"desc_en": "",
				"name_ru": "ÐÐ°ÑƒÑ€Ñƒ",
				"desc_ru": ""
			},
			{
				"mask": "+683-####",
				"cc": "NU",
				"cd": "Niue",
				"desc_en": "",
				"name_ru": "ÐÐ¸ÑƒÑ",
				"desc_ru": ""
			},
			{
				"mask": "+64(###)###-###",
				"cc": "NZ",
				"cd": "New Zealand",
				"desc_en": "",
				"name_ru": "ÐÐ¾Ð²Ð°Ñ Ð—ÐµÐ»Ð°Ð½Ð´Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+64-##-###-###",
				"cc": "NZ",
				"cd": "New Zealand",
				"desc_en": "",
				"name_ru": "ÐÐ¾Ð²Ð°Ñ Ð—ÐµÐ»Ð°Ð½Ð´Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+64(###)###-####",
				"cc": "NZ",
				"cd": "New Zealand",
				"desc_en": "",
				"name_ru": "ÐÐ¾Ð²Ð°Ñ Ð—ÐµÐ»Ð°Ð½Ð´Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+968-##-###-###",
				"cc": "OM",
				"cd": "Oman",
				"desc_en": "",
				"name_ru": "ÐžÐ¼Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+507-###-####",
				"cc": "PA",
				"cd": "Panama",
				"desc_en": "",
				"name_ru": "ÐŸÐ°Ð½Ð°Ð¼Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+51(###)###-###",
				"cc": "PE",
				"cd": "Peru",
				"desc_en": "",
				"name_ru": "ÐŸÐµÑ€Ñƒ",
				"desc_ru": ""
			},
			{
				"mask": "+689-##-##-##",
				"cc": "PF",
				"cd": "French Polynesia",
				"desc_en": "",
				"name_ru": "Ð¤Ñ€Ð°Ð½Ñ†ÑƒÐ·ÑÐºÐ°Ñ ÐŸÐ¾Ð»Ð¸Ð½ÐµÐ·Ð¸Ñ (Ð¢Ð°Ð¸Ñ‚Ð¸)",
				"desc_ru": ""
			},
			{
				"mask": "+675(###)##-###",
				"cc": "PG",
				"cd": "Papua New Guinea",
				"desc_en": "",
				"name_ru": "ÐŸÐ°Ð¿ÑƒÐ°-ÐÐ¾Ð²Ð°Ñ Ð“Ð²Ð¸Ð½ÐµÑ",
				"desc_ru": ""
			},
			{
				"mask": "+63(###)###-####",
				"cc": "PH",
				"cd": "Philippines",
				"desc_en": "",
				"name_ru": "Ð¤Ð¸Ð»Ð¸Ð¿Ð¿Ð¸Ð½Ñ‹",
				"desc_ru": ""
			},
			{
				"mask": "+92(###)###-####",
				"cc": "PK",
				"cd": "Pakistan",
				"desc_en": "",
				"name_ru": "ÐŸÐ°ÐºÐ¸ÑÑ‚Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+48(###)###-###",
				"cc": "PL",
				"cd": "Poland",
				"desc_en": "",
				"name_ru": "ÐŸÐ¾Ð»ÑŒÑˆÐ°",
				"desc_ru": ""
			},
			{
				"mask": "+970-##-###-####",
				"cc": "PS",
				"cd": "Palestine",
				"desc_en": "",
				"name_ru": "ÐŸÐ°Ð»ÐµÑÑ‚Ð¸Ð½Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+351-##-###-####",
				"cc": "PT",
				"cd": "Portugal",
				"desc_en": "",
				"name_ru": "ÐŸÐ¾Ñ€Ñ‚ÑƒÐ³Ð°Ð»Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+680-###-####",
				"cc": "PW",
				"cd": "Palau",
				"desc_en": "",
				"name_ru": "ÐŸÐ°Ð»Ð°Ñƒ",
				"desc_ru": ""
			},
			{
				"mask": "+595(###)###-###",
				"cc": "PY",
				"cd": "Paraguay",
				"desc_en": "",
				"name_ru": "ÐŸÐ°Ñ€Ð°Ð³Ð²Ð°Ð¹",
				"desc_ru": ""
			},
			{
				"mask": "+974-####-####",
				"cc": "QA",
				"cd": "Qatar",
				"desc_en": "",
				"name_ru": "ÐšÐ°Ñ‚Ð°Ñ€",
				"desc_ru": ""
			},
			{
				"mask": "+262-#####-####",
				"cc": "RE",
				"cd": "Reunion",
				"desc_en": "",
				"name_ru": "Ð ÐµÑŽÐ½ÑŒÐ¾Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+40-##-###-####",
				"cc": "RO",
				"cd": "Romania",
				"desc_en": "",
				"name_ru": "Ð ÑƒÐ¼Ñ‹Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+381-##-###-####",
				"cc": "RS",
				"cd": "Serbia",
				"desc_en": "",
				"name_ru": "Ð¡ÐµÑ€Ð±Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+7(###)###-##-##",
				"cc": "RU",
				"cd": "Russia",
				"desc_en": "",
				"name_ru": "Ð Ð¾ÑÑÐ¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+250(###)###-###",
				"cc": "RW",
				"cd": "Rwanda",
				"desc_en": "",
				"name_ru": "Ð ÑƒÐ°Ð½Ð´Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+966-5-####-####",
				"cc": "SA",
				"cd": "Saudi Arabia ",
				"desc_en": "mobile",
				"name_ru": "Ð¡Ð°ÑƒÐ´Ð¾Ð²ÑÐºÐ°Ñ ÐÑ€Ð°Ð²Ð¸Ñ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+966-#-###-####",
				"cc": "SA",
				"cd": "Saudi Arabia",
				"desc_en": "",
				"name_ru": "Ð¡Ð°ÑƒÐ´Ð¾Ð²ÑÐºÐ°Ñ ÐÑ€Ð°Ð²Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+677-###-####",
				"cc": "SB",
				"cd": "Solomon Islands ",
				"desc_en": "mobile",
				"name_ru": "Ð¡Ð¾Ð»Ð¾Ð¼Ð¾Ð½Ð¾Ð²Ñ‹ ÐžÑÑ‚Ñ€Ð¾Ð²Ð° ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+677-#####",
				"cc": "SB",
				"cd": "Solomon Islands",
				"desc_en": "",
				"name_ru": "Ð¡Ð¾Ð»Ð¾Ð¼Ð¾Ð½Ð¾Ð²Ñ‹ ÐžÑÑ‚Ñ€Ð¾Ð²Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+248-#-###-###",
				"cc": "SC",
				"cd": "Seychelles",
				"desc_en": "",
				"name_ru": "Ð¡ÐµÐ¹ÑˆÐµÐ»Ñ‹",
				"desc_ru": ""
			},
			{
				"mask": "+249-##-###-####",
				"cc": "SD",
				"cd": "Sudan",
				"desc_en": "",
				"name_ru": "Ð¡ÑƒÐ´Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+46-##-###-####",
				"cc": "SE",
				"cd": "Sweden",
				"desc_en": "",
				"name_ru": "Ð¨Ð²ÐµÑ†Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+65-####-####",
				"cc": "SG",
				"cd": "Singapore",
				"desc_en": "",
				"name_ru": "Ð¡Ð¸Ð½Ð³Ð°Ð¿ÑƒÑ€",
				"desc_ru": ""
			},
			{
				"mask": "+290-####",
				"cc": "SH",
				"cd": "Saint Helena",
				"desc_en": "",
				"name_ru": "ÐžÑÑ‚Ñ€Ð¾Ð² Ð¡Ð²ÑÑ‚Ð¾Ð¹ Ð•Ð»ÐµÐ½Ñ‹",
				"desc_ru": ""
			},
			{
				"mask": "+290-####",
				"cc": "SH",
				"cd": "Tristan da Cunha",
				"desc_en": "",
				"name_ru": "Ð¢Ñ€Ð¸ÑÑ‚Ð°Ð½-Ð´Ð°-ÐšÑƒÐ½ÑŒÑ",
				"desc_ru": ""
			},
			{
				"mask": "+386-##-###-###",
				"cc": "SI",
				"cd": "Slovenia",
				"desc_en": "",
				"name_ru": "Ð¡Ð»Ð¾Ð²ÐµÐ½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+421(###)###-###",
				"cc": "SK",
				"cd": "Slovakia",
				"desc_en": "",
				"name_ru": "Ð¡Ð»Ð¾Ð²Ð°ÐºÐ¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+232-##-######",
				"cc": "SL",
				"cd": "Sierra Leone",
				"desc_en": "",
				"name_ru": "Ð¡ÑŒÐµÑ€Ñ€Ð°-Ð›ÐµÐ¾Ð½Ðµ",
				"desc_ru": ""
			},
			{
				"mask": "+378-####-######",
				"cc": "SM",
				"cd": "San Marino",
				"desc_en": "",
				"name_ru": "Ð¡Ð°Ð½-ÐœÐ°Ñ€Ð¸Ð½Ð¾",
				"desc_ru": ""
			},
			{
				"mask": "+221-##-###-####",
				"cc": "SN",
				"cd": "Senegal",
				"desc_en": "",
				"name_ru": "Ð¡ÐµÐ½ÐµÐ³Ð°Ð»",
				"desc_ru": ""
			},
			{
				"mask": "+252-##-###-###",
				"cc": "SO",
				"cd": "Somalia",
				"desc_en": "",
				"name_ru": "Ð¡Ð¾Ð¼Ð°Ð»Ð¸",
				"desc_ru": ""
			},
			{
				"mask": "+252-#-###-###",
				"cc": "SO",
				"cd": "Somalia",
				"desc_en": "",
				"name_ru": "Ð¡Ð¾Ð¼Ð°Ð»Ð¸",
				"desc_ru": ""
			},
			{
				"mask": "+252-#-###-###",
				"cc": "SO",
				"cd": "Somalia ",
				"desc_en": "mobile",
				"name_ru": "Ð¡Ð¾Ð¼Ð°Ð»Ð¸ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+597-###-####",
				"cc": "SR",
				"cd": "Suriname ",
				"desc_en": "mobile",
				"name_ru": "Ð¡ÑƒÑ€Ð¸Ð½Ð°Ð¼ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+597-###-###",
				"cc": "SR",
				"cd": "Suriname",
				"desc_en": "",
				"name_ru": "Ð¡ÑƒÑ€Ð¸Ð½Ð°Ð¼",
				"desc_ru": ""
			},
			{
				"mask": "+211-##-###-####",
				"cc": "SS",
				"cd": "South Sudan",
				"desc_en": "",
				"name_ru": "Ð®Ð¶Ð½Ñ‹Ð¹ Ð¡ÑƒÐ´Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+239-##-#####",
				"cc": "ST",
				"cd": "Sao Tome and Principe",
				"desc_en": "",
				"name_ru": "Ð¡Ð°Ð½-Ð¢Ð¾Ð¼Ðµ Ð¸ ÐŸÑ€Ð¸Ð½ÑÐ¸Ð¿Ð¸",
				"desc_ru": ""
			},
			{
				"mask": "+503-##-##-####",
				"cc": "SV",
				"cd": "El Salvador",
				"desc_en": "",
				"name_ru": "Ð¡Ð°Ð»ÑŒÐ²Ð°Ð´Ð¾Ñ€",
				"desc_ru": ""
			},
			{
				"mask": "+1(721)###-####",
				"cc": "SX",
				"cd": "Sint Maarten",
				"desc_en": "",
				"name_ru": "Ð¡Ð¸Ð½Ñ‚-ÐœÐ°Ð°Ñ€Ñ‚ÐµÐ½",
				"desc_ru": ""
			},
			{
				"mask": "+963-##-####-###",
				"cc": "SY",
				"cd": "Syrian Arab Republic",
				"desc_en": "",
				"name_ru": "Ð¡Ð¸Ñ€Ð¸Ð¹ÑÐºÐ°Ñ Ð°Ñ€Ð°Ð±ÑÐºÐ°Ñ Ñ€ÐµÑÐ¿ÑƒÐ±Ð»Ð¸ÐºÐ°",
				"desc_ru": ""
			},
			{
				"mask": "+268-##-##-####",
				"cc": "SZ",
				"cd": "Swaziland",
				"desc_en": "",
				"name_ru": "Ð¡Ð²Ð°Ð·Ð¸Ð»ÐµÐ½Ð´",
				"desc_ru": ""
			},
			{
				"mask": "+1(649)###-####",
				"cc": "TC",
				"cd": "Turks & Caicos",
				"desc_en": "",
				"name_ru": "Ð¢Ñ‘Ñ€ÐºÑ Ð¸ ÐšÐ°Ð¹ÐºÐ¾Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+235-##-##-##-##",
				"cc": "TD",
				"cd": "Chad",
				"desc_en": "",
				"name_ru": "Ð§Ð°Ð´",
				"desc_ru": ""
			},
			{
				"mask": "+228-##-###-###",
				"cc": "TG",
				"cd": "Togo",
				"desc_en": "",
				"name_ru": "Ð¢Ð¾Ð³Ð¾",
				"desc_ru": ""
			},
			{
				"mask": "+66-##-###-####",
				"cc": "TH",
				"cd": "Thailand ",
				"desc_en": "mobile",
				"name_ru": "Ð¢Ð°Ð¸Ð»Ð°Ð½Ð´ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+66-##-###-###",
				"cc": "TH",
				"cd": "Thailand",
				"desc_en": "",
				"name_ru": "Ð¢Ð°Ð¸Ð»Ð°Ð½Ð´",
				"desc_ru": ""
			},
			{
				"mask": "+992-##-###-####",
				"cc": "TJ",
				"cd": "Tajikistan",
				"desc_en": "",
				"name_ru": "Ð¢Ð°Ð´Ð¶Ð¸ÐºÐ¸ÑÑ‚Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+690-####",
				"cc": "TK",
				"cd": "Tokelau",
				"desc_en": "",
				"name_ru": "Ð¢Ð¾ÐºÐµÐ»Ð°Ñƒ",
				"desc_ru": ""
			},
			{
				"mask": "+670-###-####",
				"cc": "TL",
				"cd": "East Timor",
				"desc_en": "",
				"name_ru": "Ð’Ð¾ÑÑ‚Ð¾Ñ‡Ð½Ñ‹Ð¹ Ð¢Ð¸Ð¼Ð¾Ñ€",
				"desc_ru": ""
			},
			{
				"mask": "+670-77#-#####",
				"cc": "TL",
				"cd": "East Timor",
				"desc_en": "Timor Telecom",
				"name_ru": "Ð’Ð¾ÑÑ‚Ð¾Ñ‡Ð½Ñ‹Ð¹ Ð¢Ð¸Ð¼Ð¾Ñ€",
				"desc_ru": "Timor Telecom"
			},
			{
				"mask": "+670-78#-#####",
				"cc": "TL",
				"cd": "East Timor",
				"desc_en": "Timor Telecom",
				"name_ru": "Ð’Ð¾ÑÑ‚Ð¾Ñ‡Ð½Ñ‹Ð¹ Ð¢Ð¸Ð¼Ð¾Ñ€",
				"desc_ru": "Timor Telecom"
			},
			{
				"mask": "+993-#-###-####",
				"cc": "TM",
				"cd": "Turkmenistan",
				"desc_en": "",
				"name_ru": "Ð¢ÑƒÑ€ÐºÐ¼ÐµÐ½Ð¸ÑÑ‚Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+216-##-###-###",
				"cc": "TN",
				"cd": "Tunisia",
				"desc_en": "",
				"name_ru": "Ð¢ÑƒÐ½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+676-#####",
				"cc": "TO",
				"cd": "Tonga",
				"desc_en": "",
				"name_ru": "Ð¢Ð¾Ð½Ð³Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+90(###)###-####",
				"cc": "TR",
				"cd": "Turkey",
				"desc_en": "",
				"name_ru": "Ð¢ÑƒÑ€Ñ†Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+1(868)###-####",
				"cc": "TT",
				"cd": "Trinidad & Tobago",
				"desc_en": "",
				"name_ru": "Ð¢Ñ€Ð¸Ð½Ð¸Ð´Ð°Ð´ Ð¸ Ð¢Ð¾Ð±Ð°Ð³Ð¾",
				"desc_ru": ""
			},
			{
				"mask": "+688-90####",
				"cc": "TV",
				"cd": "Tuvalu ",
				"desc_en": "mobile",
				"name_ru": "Ð¢ÑƒÐ²Ð°Ð»Ñƒ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+688-2####",
				"cc": "TV",
				"cd": "Tuvalu",
				"desc_en": "",
				"name_ru": "Ð¢ÑƒÐ²Ð°Ð»Ñƒ",
				"desc_ru": ""
			},
			{
				"mask": "+886-#-####-####",
				"cc": "TW",
				"cd": "Taiwan",
				"desc_en": "",
				"name_ru": "Ð¢Ð°Ð¹Ð²Ð°Ð½ÑŒ",
				"desc_ru": ""
			},
			{
				"mask": "+886-####-####",
				"cc": "TW",
				"cd": "Taiwan",
				"desc_en": "",
				"name_ru": "Ð¢Ð°Ð¹Ð²Ð°Ð½ÑŒ",
				"desc_ru": ""
			},
			{
				"mask": "+255-##-###-####",
				"cc": "TZ",
				"cd": "Tanzania",
				"desc_en": "",
				"name_ru": "Ð¢Ð°Ð½Ð·Ð°Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+380(##)###-##-##",
				"cc": "UA",
				"cd": "Ukraine",
				"desc_en": "",
				"name_ru": "Ð£ÐºÑ€Ð°Ð¸Ð½Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+256(###)###-###",
				"cc": "UG",
				"cd": "Uganda",
				"desc_en": "",
				"name_ru": "Ð£Ð³Ð°Ð½Ð´Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+44-##-####-####",
				"cc": "UK",
				"cd": "United Kingdom",
				"desc_en": "",
				"name_ru": "Ð’ÐµÐ»Ð¸ÐºÐ¾Ð±Ñ€Ð¸Ñ‚Ð°Ð½Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+598-#-###-##-##",
				"cc": "UY",
				"cd": "Uruguay",
				"desc_en": "",
				"name_ru": "Ð£Ñ€ÑƒÐ³Ð²Ð°Ð¹",
				"desc_ru": ""
			},
			{
				"mask": "+998-##-###-####",
				"cc": "UZ",
				"cd": "Uzbekistan",
				"desc_en": "",
				"name_ru": "Ð£Ð·Ð±ÐµÐºÐ¸ÑÑ‚Ð°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+39-6-698-#####",
				"cc": "VA",
				"cd": "Vatican City",
				"desc_en": "",
				"name_ru": "Ð’Ð°Ñ‚Ð¸ÐºÐ°Ð½",
				"desc_ru": ""
			},
			{
				"mask": "+1(784)###-####",
				"cc": "VC",
				"cd": "Saint Vincent & the Grenadines",
				"desc_en": "",
				"name_ru": "Ð¡ÐµÐ½Ñ‚-Ð’Ð¸Ð½ÑÐµÐ½Ñ‚ Ð¸ Ð“Ñ€ÐµÐ½Ð°Ð´Ð¸Ð½Ñ‹",
				"desc_ru": ""
			},
			{
				"mask": "+58(###)###-####",
				"cc": "VE",
				"cd": "Venezuela",
				"desc_en": "",
				"name_ru": "Ð’ÐµÐ½ÐµÑÑƒÑÐ»Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+1(284)###-####",
				"cc": "VG",
				"cd": "British Virgin Islands",
				"desc_en": "",
				"name_ru": "Ð‘Ñ€Ð¸Ñ‚Ð°Ð½ÑÐºÐ¸Ðµ Ð’Ð¸Ñ€Ð³Ð¸Ð½ÑÐºÐ¸Ðµ Ð¾ÑÑ‚Ñ€Ð¾Ð²Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+1(340)###-####",
				"cc": "VI",
				"cd": "US Virgin Islands",
				"desc_en": "",
				"name_ru": "ÐÐ¼ÐµÑ€Ð¸ÐºÐ°Ð½ÑÐºÐ¸Ðµ Ð’Ð¸Ñ€Ð³Ð¸Ð½ÑÐºÐ¸Ðµ Ð¾ÑÑ‚Ñ€Ð¾Ð²Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+84-##-####-###",
				"cc": "VN",
				"cd": "Vietnam",
				"desc_en": "",
				"name_ru": "Ð’ÑŒÐµÑ‚Ð½Ð°Ð¼",
				"desc_ru": ""
			},
			{
				"mask": "+84(###)####-###",
				"cc": "VN",
				"cd": "Vietnam",
				"desc_en": "",
				"name_ru": "Ð’ÑŒÐµÑ‚Ð½Ð°Ð¼",
				"desc_ru": ""
			},
			{
				"mask": "+678-##-#####",
				"cc": "VU",
				"cd": "Vanuatu ",
				"desc_en": "mobile",
				"name_ru": "Ð’Ð°Ð½ÑƒÐ°Ñ‚Ñƒ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+678-#####",
				"cc": "VU",
				"cd": "Vanuatu",
				"desc_en": "",
				"name_ru": "Ð’Ð°Ð½ÑƒÐ°Ñ‚Ñƒ",
				"desc_ru": ""
			},
			{
				"mask": "+681-##-####",
				"cc": "WF",
				"cd": "Wallis and Futuna",
				"desc_en": "",
				"name_ru": "Ð£Ð¾Ð»Ð»Ð¸Ñ Ð¸ Ð¤ÑƒÑ‚ÑƒÐ½Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+685-##-####",
				"cc": "WS",
				"cd": "Samoa",
				"desc_en": "",
				"name_ru": "Ð¡Ð°Ð¼Ð¾Ð°",
				"desc_ru": ""
			},
			{
				"mask": "+967-###-###-###",
				"cc": "YE",
				"cd": "Yemen ",
				"desc_en": "mobile",
				"name_ru": "Ð™ÐµÐ¼ÐµÐ½ ",
				"desc_ru": "Ð¼Ð¾Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ðµ"
			},
			{
				"mask": "+967-#-###-###",
				"cc": "YE",
				"cd": "Yemen",
				"desc_en": "",
				"name_ru": "Ð™ÐµÐ¼ÐµÐ½",
				"desc_ru": ""
			},
			{
				"mask": "+967-##-###-###",
				"cc": "YE",
				"cd": "Yemen",
				"desc_en": "",
				"name_ru": "Ð™ÐµÐ¼ÐµÐ½",
				"desc_ru": ""
			},
			{
				"mask": "+27-##-###-####",
				"cc": "ZA",
				"cd": "South Africa",
				"desc_en": "",
				"name_ru": "Ð®Ð¶Ð½Ð¾-ÐÑ„Ñ€Ð¸ÐºÐ°Ð½ÑÐºÐ°Ñ Ð ÐµÑÐ¿.",
				"desc_ru": ""
			},
			{
				"mask": "+260-##-###-####",
				"cc": "ZM",
				"cd": "Zambia",
				"desc_en": "",
				"name_ru": "Ð—Ð°Ð¼Ð±Ð¸Ñ",
				"desc_ru": ""
			},
			{
				"mask": "+263-#-######",
				"cc": "ZW",
				"cd": "Zimbabwe",
				"desc_en": "",
				"name_ru": "Ð—Ð¸Ð¼Ð±Ð°Ð±Ð²Ðµ",
				"desc_ru": ""
			},
			{
				"mask": "+1(###)###-####",
				"cc": ["US", "CA"],
				"cd": "USA and Canada",
				"desc_en": "",
				"name_ru": "Ð¡Ð¨Ð Ð¸ ÐšÐ°Ð½Ð°Ð´Ð°",
				"desc_ru": ""
			}
			]
		}
	});

	return Inputmask;
}));

