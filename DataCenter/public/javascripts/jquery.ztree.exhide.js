/*
 * JQuery zTree exHideNodes v3.5.23
 * http://zTree.me/
 *
 * Copyright (c) 2010 Hunter.z
 *
 * Licensed same as jquery - MIT License
 * http://www.opensource.org/licenses/mit-license.php
 *
 * email: hunter.z@263.net
 * Date: 2016-04-01
 */
(function($){
	//default init node of exLib
	var _initNode = function(setting, level, n, parentNode, isFirstNode, isLastNode, openFlag) {
		if (typeof n.isHidden == "string") n.isHidden = tools.eqs(n.isHidden, "true");
		n.isHidden = !!n.isHidden;
		data.initHideForExCheck(setting, n);
	},
	//add dom for check
	_beforeA = function(setting, node, html) {},
	//update zTreeObj, add method of exLib
	_zTreeTools = function(setting, zTreeTools) {
		zTreeTools.showNodes = function(nodes, options) {
			view.showNodes(setting, nodes, options);
		}
		zTreeTools.showNode = function(node, options) {
			if (!node) {
				return;
			}
			view.showNodes(setting, [node], options);
		}
		zTreeTools.hideNodes = function(nodes, options) {
			view.hideNodes(setting, nodes, options);
		}
		zTreeTools.hideNode = function(node, options) {
			if (!node) {
				return;
			}
			view.hideNodes(setting, [node], options);
		}

		var _checkNode = zTreeTools.checkNode;
		if (_checkNode) {
			zTreeTools.checkNode = function(node, checked, checkTypeFlag, callbackFlag) {
				if (!!node && !!node.isHidden) {
					return;
				}
				_checkNode.apply(zTreeTools, arguments);
			}
		}
	},
	//method of operate data
	_data = {
		initHideForExCheck: function(setting, n) {
			if (n.isHidden && setting.check && setting.check.enable) {
				if(typeof n._nocheck == "undefined") {
					n._nocheck = !!n.nocheck
					n.nocheck = true;
				}
				n.check_Child_State = -1;
				if (view.repairParentChkClassWithSelf) {
					view.repairParentChkClassWithSelf(setting, n);
				}
			}
		},
		initShowForExCheck: function(setting, n) {
			if (!n.isHidden && setting.check && setting.check.enable) {
				if(typeof n._nocheck != "undefined") {
					n.nocheck = n._nocheck;
					delete n._nocheck;
				}
				if (view.setChkClass) {
					var checkObj = $$(n, consts.id.CHECK, setting);
					view.setChkClass(setting, checkObj, n);
				}
				if (view.repairParentChkClassWithSelf) {
					view.repairParentChkClassWithSelf(setting, n);
				}
			}
		}
	},
	//method of operate ztree dom
	_view = {
		clearOldFirstNode: function(setting, node) {
			var n = node.getNextNode();
			while(!!n){
				if (n.isFirstNode) {
					n.isFirstNode = false;
					view.setNodeLineIcos(setting, n);
					break;
				}
				if (n.isLastNode) {
					break;
				}
				n = n.getNextNode();
			}
		},
        clearOldLastNode: function(setting, node, openFlag) {
            var n = node.getPreNode();
            while(!!n){
                if (n.isLastNode) {
                    n.isLastNode = false;
                    if (openFlag) {
                        view.setNodeLineIcos(setting, n);
                    }
                    break;
                }
                if (n.isFirstNode) {
                    break;
                }
                n = n.getPreNode();
            }
        },
		makeDOMNodeMainBefore: function(html, setting, node) {
			html.push("<li ", (node.isHidden ? "style='display:none;' " : ""), "id='", node.tId, "' class='", consts.className.LEVEL, node.level,"' tabindex='0' hidefocus='true' treenode>");
		},
		showNode: function(setting, node, options) {
			node.isHidden = false;
			data.initShowForExCheck(setting, node);
			$$(node, setting).show();
		},
		showNodes: function(setting, nodes, options) {
			if (!nodes || nodes.length == 0) {
				return;
			}
			var pList = {}, i, j;
			for (i=0, j=nodes.length; i<j; i++) {
				var n = nodes[i];
				if (!pList[n.parentTId]) {
					var pn = n.getParentNode();
					pList[n.parentTId] = (pn === null) ? data.getRoot(setting) : n.getParentNode();
				}
				view.showNode(setting, n, options);
			}
			for (var tId in pList) {
				var children = pList[tId][setting.data.key.children];
				view.setFirstNodeForShow(setting, children);
				view.setLastNodeForShow(setting, children);
			}
		},
		hideNode: function(setting, node, options) {
			node.isHidden = true;
			node.isFirstNode = false;
			node.isLastNode = false;
			data.initHideForExCheck(setting, node);
			view.cancelPreSelectedNode(setting, node);
			$$(node, setting).hide();
		},
		hideNodes: function(setting, nodes, options) {
			if (!nodes || nodes.length == 0) {
				return;
			}
			var pList = {}, i, j;
			for (i=0, j=nodes.length; i<j; i++) {
				var n = nodes[i];
				if ((n.isFirstNode || n.isLastNode) && !pList[n.parentTId]) {
					var pn = n.getParentNode();
					pList[n.parentTId] = (pn === null) ? data.getRoot(setting) : n.getParentNode();
				}
				view.hideNode(setting, n, options);
			}
			for (var tId in pList) {
				var children = pList[tId][setting.data.key.children];
				view.setFirstNodeForHide(setting, children);
				view.setLastNodeForHide(setting, children);
			}
		},
		setFirstNode: function(setting, parentNode) {
			var childKey = setting.data.key.children, childLength = parentNode[childKey].length;
			if (childLength > 0 && !parentNode[childKey][0].isHidden) {
				parentNode[childKey][0].isFirstNode = true;
			} else if (childLength > 0) {
				view.setFirstNodeForHide(setting, parentNode[childKey]);
			}
		},
		setLastNode: function(setting, parentNode) {
			var childKey = setting.data.key.children, childLength = parentNode[childKey].length;
			if (childLength > 0 && !parentNode[childKey][0].isHidden) {
				parentNode[childKey][childLength - 1].isLastNode = true;
			} else if (childLength > 0) {
				view.setLastNodeForHide(setting, parentNode[childKey]);
			}
		},
		setFirstNodeForHide: function(setting, nodes) {
			var n,i,j;
			for (i=0, j=nodes.length; i<j; i++) {
				n = nodes[i];
				if (n.isFirstNode) {
					break;
				}
				if (!n.isHidden && !n.isFirstNode) {
					n.isFirstNode = true;
					view.setNodeLineIcos(setting, n);
					break;
				} else {
					n = null;
				}
			}
			return n;
		},
		setFirstNodeForShow: function(setting, nodes) {
			var n,i,j, first, old;
			for(i=0, j=nodes.length; i<j; i++) {
				n = nodes[i];
				if (!first && !n.isHidden && n.isFirstNode) {
					first = n;
					break;
				} else if (!first && !n.isHidden && !n.isFirstNode) {
					n.isFirstNode = true;
					first = n;
					view.setNodeLineIcos(setting, n);
				} else if (first && n.isFirstNode) {
					n.isFirstNode = false;
					old = n;
					view.setNodeLineIcos(setting, n);
					break;
				} else {
					n = null;
				}
			}
			return {"new":first, "old":old};
		},
		setLastNodeForHide: function(setting, nodes) {
			var n,i;
			for (i=nodes.length-1; i>=0; i--) {
				n = nodes[i];
				if (n.isLastNode) {
					break;
				}
				if (!n.isHidden && !n.isLastNode) {
					n.isLastNode = true;
					view.setNodeLineIcos(setting, n);
					break;
				} else {
					n = null;
				}
			}
			return n;
		},
		setLastNodeForShow: function(setting, nodes) {
			var n,i,j, last, old;
			for (i=nodes.length-1; i>=0; i--) {
				n = nodes[i];
				if (!last && !n.isHidden && n.isLastNode) {
					last = n;
					break;
				} else if (!last && !n.isHidden && !n.isLastNode) {
					n.isLastNode = true;
					last = n;
					view.setNodeLineIcos(setting, n);
				} else if (last && n.isLastNode) {
					n.isLastNode = false;
					old = n;
					view.setNodeLineIcos(setting, n);
					break;
				} else {
					n = null;
				}
			}
			return {"new":last, "old":old};
		}
	},

	_z = {
		view: _view,
		data: _data
	};
	$.extend(true, $.fn.zTree._z, _z);

	var zt = $.fn.zTree,
	tools = zt._z.tools,
	consts = zt.consts,
	view = zt._z.view,
	data = zt._z.data,
	event = zt._z.event,
	$$ = tools.$;

	data.addInitNode(_initNode);
	data.addBeforeA(_beforeA);
	data.addZTreeTools(_zTreeTools);

//	Override method in core
	var _dInitNode = data.initNode;
    data.initNode = function(setting, level, node, parentNode, isFirstNode, isLastNode, openFlag) {
        var tmpPNode = (parentNode) ? parentNode: data.getRoot(setting),
            children = tmpPNode[setting.data.key.children];
        data.tmpHideFirstNode = view.setFirstNodeForHide(setting, children);
        data.tmpHideLastNode = view.setLastNodeForHide(setting, children);
        if (openFlag) {
            view.setNodeLineIcos(setting, data.tmpHideFirstNode);
            view.setNodeLineIcos(setting, data.tmpHideLastNode);
        }
        isFirstNode = (data.tmpHideFirstNode === node);
        isLastNode = (data.tmpHideLastNode === node);
        if (_dInitNode) _dInitNode.apply(data, arguments);
        if (openFlag && isLastNode) {
            view.clearOldLastNode(setting, node, openFlag);
        }
    };

	var _makeChkFlag = data.makeChkFlag;
	if (!!_makeChkFlag) {
		data.makeChkFlag = function(setting, node) {
			if (!!node && !!node.isHidden) {
				return;
			}
			_makeChkFlag.apply(data, arguments);
		}
	}

	var _getTreeCheckedNodes = data.getTreeCheckedNodes;
	if (!!_getTreeCheckedNodes) {
		data.getTreeCheckedNodes = function(setting, nodes, checked, results) {
			if (!!nodes && nodes.length > 0) {
				var p = nodes[0].getParentNode();
				if (!!p && !!p.isHidden) {
					return [];
				}
			}
			return _getTreeCheckedNodes.apply(data, arguments);
		}
	}

	var _getTreeChangeCheckedNodes = data.getTreeChangeCheckedNodes;
	if (!!_getTreeChangeCheckedNodes) {
		data.getTreeChangeCheckedNodes = function(setting, nodes, results) {
			if (!!nodes && nodes.length > 0) {
				var p = nodes[0].getParentNode();
				if (!!p && !!p.isHidden) {
					return [];
				}
			}
			return _getTreeChangeCheckedNodes.apply(data, arguments);
		}
	}

	var _expandCollapseSonNode = view.expandCollapseSonNode;
	if (!!_expandCollapseSonNode) {
		view.expandCollapseSonNode = function(setting, node, expandFlag, animateFlag, callback) {
			if (!!node && !!node.isHidden) {
				return;
			}
			_expandCollapseSonNode.apply(view, arguments);
		}
	}

	var _setSonNodeCheckBox = view.setSonNodeCheckBox;
	if (!!_setSonNodeCheckBox) {
		view.setSonNodeCheckBox = function(setting, node, value, srcNode) {
			if (!!node && !!node.isHidden) {
				return;
			}
			_setSonNodeCheckBox.apply(view, arguments);
		}
	}

	var _repairParentChkClassWithSelf = view.repairParentChkClassWithSelf;
	if (!!_repairParentChkClassWithSelf) {
		view.repairParentChkClassWithSelf = function(setting, node) {
			if (!!node && !!node.isHidden) {
				return;
			}
			_repairParentChkClassWithSelf.apply(view, arguments);
		}
	}
})(jQuery);