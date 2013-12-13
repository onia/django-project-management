Ext.QuickTips.init();

Ext.state.Manager.setProvider(new Ext.state.CookieProvider());

Ext.namespace('Ext.ux.tree');
Ext.ux.tree.State = function(config) {
   Ext.apply(this, config);
};
Ext.extend(Ext.ux.tree.State, Ext.util.Observable, {
   init: function(tree) {
      this.tree = tree;
      this.stateName = 'TreePanelState_' + this.tree.id;
      this.idField = this.idField || 'id';
      this.provider = Ext.state.Manager.getProvider() || new Ext.state.CookieProvider();
      this.state = this.provider.get(this.stateName, {});
      this.tree.on({
         scope: this,
         collapsenode: this.onCollapse,
         expandnode: this.onExpand,
         append: this.onNodeAdded
      });
   },
    
   saveState : function(newState) {
      this.state = newState || this.state;
      this.provider.set(this.stateName, this.state);
   },
    
   onNodeAdded: function(tree, parentNode, node, index) {	
      switch (this.state[node.id]) {
         case 'C': 
            node.expanded = false; 
            break;
         case 'E': 
            node.expanded = true; 
            break;
      };
   },
   
   onExpand: function(node) {
      this.state[node.id] = 'E';
      this.saveState();
   },
   
   onCollapse: function(node) {
      this.state[node.id] = 'C';
      this.saveState();
   }

});

Ext.DatePicker.prototype.startDay = 1;


// Function for Ajax mouseover tooltips on form fields
Ext.override(Ext.form.Field, {
    afterRender: function() {
        var label = findLabel(this);
        if(label){                                  
 			if(this.ttEnabled){
            	new Ext.ToolTip({
                	target: label,
                	width: 250,
                	autoLoad: {
                    	url: '/GetDoc/', 
                    	params : { 
                        	field : this.cmsSlug
                    	}
                	}
            	});
			}
       }
       Ext.form.Field.superclass.afterRender.call(this);
       this.initEvents(); 
  }
});

var findLabel = function(field) {  
    var wrapDiv = null;
    var label = null
    wrapDiv = field.getEl().up('div.x-form-item');    
    if(wrapDiv) {
        label = wrapDiv.child('label');        
    }
    if(label) {
        return label;
    }    
}  

// Function for message passing boxes

Ext.message = function(){
    var msgCt;
	function createBox(t, s){
		// Added msg id
        return ['<div class="msg" id="msg" name="msg">',
                '<div class="x-box-tl"><div class="x-box-tr"><div class="x-box-tc"></div></div></div>',
                '<div class="x-box-ml"><div class="x-box-mr"><div class="x-box-mc"><h3>', t, '</h3>', s, '</div></div></div>',
                '<div class="x-box-bl"><div class="x-box-br"><div class="x-box-bc"></div></div></div>',
                '</div>'].join('');
    }  
	return {
	msg : function(title, format, sec){
            if(!msgCt){
                msgCt = Ext.DomHelper.insertFirst(document.body, {id:'msg-div'}, true);
            }
            
            var s = String.format.apply(String, Array.prototype.slice.call(arguments, 1));
            var m = Ext.DomHelper.append(msgCt, {html:createBox(title, s)}, true);
            // Added The following code to get the <div> height
            var yoffset = document.getElementById("msg").style.height;
            // Then added that value to the yoffset position in alignTo 
            msgCt.alignTo(document, 'br-br', [0,yoffset]);
            m.slideIn('t').pause(sec).ghost("t", {remove:true});
        }  
    }
}();

// Plugin for grid drag and drop
Ext.namespace('Ext.ux.dd');

Ext.ux.dd.GridDragDropRowOrder = Ext.extend(Ext.util.Observable,
{
    copy: false,
    scrollable: false,
    constructor : function(config)
    {
        if (config)
            Ext.apply(this, config);
        this.addEvents(
        {
            beforerowmove: true,
            afterrowmove: true,
            beforerowcopy: true,
            afterrowcopy: true
        });
       Ext.ux.dd.GridDragDropRowOrder.superclass.constructor.call(this);
    },
    init : function (grid)
    {
        this.grid = grid;
        grid.enableDragDrop = true;
        grid.on({
            render: { fn: this.onGridRender, scope: this, single: true }
        });
    },
    onGridRender : function (grid)
    {
        var self = this;
        this.target = new Ext.dd.DropTarget(grid.getEl(),
        {
            ddGroup: grid.ddGroup || 'GridDD',
            grid: grid,
            gridDropTarget: this,
            notifyDrop: function(dd, e, data)
            {
                // Remove drag lines. The 'if' condition prevents null error when drop occurs without dragging out of the selection area
                if (this.currentRowEl)
                {
                    this.currentRowEl.removeClass('grid-row-insert-below');
                    this.currentRowEl.removeClass('grid-row-insert-above');
                }

                // determine the row
                var t = Ext.lib.Event.getTarget(e);
                var rindex = this.grid.getView().findRowIndex(t);
                if (rindex === false || rindex == data.rowIndex)
                {
                    return false;
                }
                // fire the before move/copy event
                if (this.gridDropTarget.fireEvent(self.copy ? 'beforerowcopy' : 'beforerowmove', this.gridDropTarget, data.rowIndex, rindex, data.selections, 123) === false)
                {
                    return false;
                }

                // update the store
                var ds = this.grid.getStore();

                // Changes for multiselction by Spirit
                var selections = new Array();
                var keys = ds.data.keys;
                for (var key in keys)
                {
                    for (var i = 0; i < data.selections.length; i++)
                    {
                        if (keys[key] == data.selections[i].id)
                        {
                            // Exit to prevent drop of selected records on itself.
                            if (rindex == key)
                            {
                                return false;
                            }
                            selections.push(data.selections[i]);
                        }
                    }
                }

                // fix rowindex based on before/after move
                if (rindex > data.rowIndex && this.rowPosition < 0)
                {
                    rindex--;
                }
                if (rindex < data.rowIndex && this.rowPosition > 0)
                {
                    rindex++;
                }

                // fix rowindex for multiselection
                if (rindex > data.rowIndex && data.selections.length > 1)
                {
                    rindex = rindex - (data.selections.length - 1);
                }

                // we tried to move this node before the next sibling, we stay in place
                if (rindex == data.rowIndex)
                {
                    return false;
                }

                // fire the before move/copy event
                /* dupe - does it belong here or above???
                if (this.gridDropTarget.fireEvent(self.copy ? 'beforerowcopy' : 'beforerowmove', this.gridDropTarget, data.rowIndex, rindex, data.selections, 123) === false)
                {
                    return false;
                }
                */

                if (!self.copy)
                {
                    for (var i = 0; i < data.selections.length; i++)
                    {
                        ds.remove(ds.getById(data.selections[i].id));
                    }
                }

                for (var i = selections.length - 1; i >= 0; i--)
                {
                    var insertIndex = rindex;
                    ds.insert(insertIndex, selections[i]);
                }

                // re-select the row(s)
                var sm = this.grid.getSelectionModel();
                if (sm)
                {
                    sm.selectRecords(data.selections);
                }

                // fire the after move/copy event
                this.gridDropTarget.fireEvent(self.copy ? 'afterrowcopy' : 'afterrowmove', this.gridDropTarget, data.rowIndex, rindex, data.selections);
                return true;
            },

            notifyOver: function(dd, e, data)
            {
                var t = Ext.lib.Event.getTarget(e);
                var rindex = this.grid.getView().findRowIndex(t);

                // Similar to the code in notifyDrop. Filters for selected rows and quits function if any one row matches the current selected row.
                var ds = this.grid.getStore();
                var keys = ds.data.keys;
                for (var key in keys)
                {
                    for (var i = 0; i < data.selections.length; i++)
                    {
                        if (keys[key] == data.selections[i].id)
                        {
                            if (rindex == key)
                            {
                                if (this.currentRowEl)
                                {
                                    this.currentRowEl.removeClass('grid-row-insert-below');
                                    this.currentRowEl.removeClass('grid-row-insert-above');
                                }
                                return this.dropNotAllowed;
                            }
                        }
                    }
                }

                // If on first row, remove upper line. Prevents negative index error as a result of rindex going negative.
                if (rindex < 0 || rindex === false)
                {
                    this.currentRowEl.removeClass('grid-row-insert-above');
                    return this.dropNotAllowed;
                }

                try
                {
                    var currentRow = this.grid.getView().getRow(rindex);
                    // Find position of row relative to page (adjusting for grid's scroll position)
                    var resolvedRow = new Ext.Element(currentRow).getY() - this.grid.getView().scroller.dom.scrollTop;
                    var rowHeight = currentRow.offsetHeight;

                    // Cursor relative to a row. -ve value implies cursor is above the row's middle and +ve value implues cursor is below the row's middle.
                    this.rowPosition = e.getPageY() - resolvedRow - (rowHeight/2);

                    // Clear drag line.
                    if (this.currentRowEl)
                    {
                        this.currentRowEl.removeClass('grid-row-insert-below');
                        this.currentRowEl.removeClass('grid-row-insert-above');
                    }

                    if (this.rowPosition > 0)
                    {
                        // If the pointer is on the bottom half of the row.
                        this.currentRowEl = new Ext.Element(currentRow);
                        this.currentRowEl.addClass('grid-row-insert-below');
                    }
                    else
                    {
                        // If the pointer is on the top half of the row.
                        if (rindex - 1 >= 0)
                        {
                            var previousRow = this.grid.getView().getRow(rindex - 1);
                            this.currentRowEl = new Ext.Element(previousRow);
                            this.currentRowEl.addClass('grid-row-insert-below');
                        }
                        else
                        {
                            // If the pointer is on the top half of the first row.
                            this.currentRowEl.addClass('grid-row-insert-above');
                        }
                    }
                }
                catch (err)
                {
                    console.warn(err);
                    rindex = false;
                }
                return (rindex === false)? this.dropNotAllowed : this.dropAllowed;
            },

            notifyOut: function(dd, e, data)
            {
                // Remove drag lines when pointer leaves the gridView.
                if (this.currentRowEl)
                {
                    this.currentRowEl.removeClass('grid-row-insert-above');
                    this.currentRowEl.removeClass('grid-row-insert-below');
                }
            }
        });

        if (this.targetCfg)
        {
            Ext.apply(this.target, this.targetCfg);
        }

        if (this.scrollable)
        {
            Ext.dd.ScrollManager.register(grid.getView().getEditorParent());
            grid.on({
                beforedestroy: this.onBeforeDestroy,
                scope: this,
                single: true
            });
        }
    },

    getTarget: function()
    {
        return this.target;
    },

    getGrid: function()
    {
        return this.grid;
    },

    getCopy: function()
    {
        return this.copy ? true : false;
    },

    setCopy: function(b)
    {
        this.copy = b ? true : false;
    },

    onBeforeDestroy : function (grid)
    {
        // if we previously registered with the scroll manager, unregister
        // it (if we don't it will lead to problems in IE)
        Ext.dd.ScrollManager.unregister(grid.getView().getEditorParent());
    }
});


// Navigation tree
var tree_data = [
					{ text: 'Projects', id: 'projectsNode', leaf: false, children: [{ text: 'View Dashboard', href: "/", leaf: true }]},
  					{ text: 'Work In Progress', id: 'wipNode', leaf: false, children: [{ text: "All WIP Reports", href: "/WIP/", leaf: true},
                        { text: "My WIP Items", href: "/WIP/MyWIP/", leaf: true }] },
  					{ text: 'Rota', id: 'rotaNode', leaf: false,
    					children: [{ text: "All Rotas", href: "/Rota/ViewAll/", leaf: true}, { text: "My Teams Rota", href: "/Rota/ViewMyTeam/", leaf: true }, { text: "My Rota", href: "/Rota/ViewMyRota/", leaf: true } ]},
  					{ text: 'Documentation', id: 'docNode', leaf: false,
    					children: [{ text: "Help Files", href: "/en/", leaf: true}, { text: "Bugs/Source code", href: "http://code.google.com/p/django-project-management", leaf: true }] },
  					{ text: 'My Account', id: 'accountNode', leaf: false,
    					children: [{ text: "Log out", href: "/accounts/logout/", leaf: true}] }
			
				]

var rootNode = new Ext.tree.AsyncTreeNode({ text: 'Root', children: tree_data });
var tree = new Ext.tree.TreePanel({ root: rootNode, border: false, plugins: [new Ext.ux.tree.State()], rootVisible: false, stateful: true, stateId: "nav_tree"});
	
    	
var center_html_content = { xtype: "panel", contentEl: "center_panel_html", bodyStyle: "padding: 15px;"}
//var new_menu = { xtype: "tbbutton", text: "New", menu: [{ text: "New Project", href: "/Projects/New"}, { text: "New WIP Report", href: "/WIP/NEW" }]}
//var toolbar = new Ext.Toolbar({ items: [ new_menu ] });
var toolbar = new Ext.Toolbar({ items: [ ] });

var center_panel = { xtype: "panel", region: "center", items: [ toolbar, center_html_content ], bodyStyle: "padding: 0px;", autoScroll: true}
var west_panel = { xtype: "panel", title: 'Navigation', region: 'west', margins: '0 0 0 0',
					cmargins: '0 5 0 0', width: 175, minSize: 100, maxSize: 250, items: [ tree ] }
					
					
					
