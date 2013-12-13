
/* Some constants used in forms and grids */
var GRID_HEIGHT = 210;
var GRID_WIDTH = 500;
var TEXTAREA_WIDTH = 400;
var TEXTAREA_HEIGHT = 80; 


/*
 * Create work item grid
 */

var st_wip_items = new Ext.data.GroupingStore({
	proxy: new Ext.data.HttpProxy({ url: "/WIP/MyWIP/?xhr" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [
		{ name: "pk", mapping: "pk" },
		{ name: "status", mapping: "fields.status" },
		{ name: "heading", mapping: "extras.get_heading" },
		{ name: "modified_date", mapping: "fields.modified_date" },
		{ name: "created_date", mapping: "fields.created_date" },
		{ name: "description", mapping: "fields.description" },
		{ name: "assignee", mapping: "fields.assignee.extras.get_full_name" },
		{ name: "deadline", mapping: "fields.deadline" },
		{ name: "complete", mapping: "fields.complete", type: 'bool' },
		{ name: "objective", mapping: "fields.objective", type: 'bool' },
		{ name: "engineering_days", mapping: "extras.get_engineering_days_as_ul" },
		{ name: "history", mapping: "fields.history" },
		{ name: "history_html", mapping: "extras.get_history_html" }
	]}), 
	sortInfo:{field: 'assignee', direction: "ASC"},
	groupField:'heading',
	autoLoad: true
});

var grid_wip_items = new Ext.grid.GridPanel({
	store: st_wip_items,
	id: "grid_wip_items",
	columns: [
		new Ext.grid.RowNumberer(),
		{ header: "Heading", dataIndex: "heading", sortable: true, hidden: true }, 
		{ header: "Status", dataIndex: "status", sortable: true, hidden: true }, 
		{ header: "Modified Date", dataIndex: "modified_date", sortable:true, hidden: true },
		{ header: "Created Date", dataIndex: "created_date", sortable:true, hidden: true },
		{ header: "Description", dataIndex: "description", sortable:true },
		{ header: "Assignee", dataIndex: "assignee", sortable:true },
		{ header: "Deadline", dataIndex: "deadline", sortable:true, hidden: true },
		{ xtype: 'booleancolumn', header: "Complete", dataIndex: "complete", sortable:true, hidden: true,
			trueText: 'Yes', falseText: 'No', editor: { xtype: 'checkbox' } },
		{ xtype: 'booleancolumn', header: "Objective", dataIndex: "objective", sortable:true, 
			trueText: 'Yes', falseText: 'No', editor: { xtype: 'checkbox' } },
		{ header: "Engineering Days", dataIndex: "engineering_days", sortable:true, hidden: true }
	],
	sm: new Ext.grid.RowSelectionModel({singleSelect: true}),
	view: new Ext.grid.GroupingView({
            forceFit:true,
            groupTextTpl: '{text} ({[values.rs.length]} {[values.rs.length > 1 ? "Items" : "Item"]})'
    }),
    height: GRID_HEIGHT,
	width: GRID_WIDTH,
	split: true,
	region: 'west'
});


var wip_item_markup = [
		'<table class="project_table">',
		'<tr><th>Status</th> <td>{status}</td></tr>',
		'<tr><th>Modified Date</th> <td>{modified_date}</td></tr>',
		'<tr><th>Created Date</th> <td>{created_date}</td></tr>',
		'<tr><th>Description</th> <td>{description}</td></tr>',
		'<tr><th>Assignee</th> <td>{assignee}</td></tr>',
		'<tr><th>Deadline</th> <td>{deadline}</td</tr>',
		'<tr><th>Complete</th> <td>{complete}</td></tr>',
		'<tr><th>Objective</th> <td>{objective}</td></tr>',
		'<tr><th>Engineering Days</th> <td>{engineering_days}</td></tr>',
		'<tr><th>History</th> <td>{history_html}</td></tr>', '</table>' ];
var wipItemTpl = new Ext.Template(wip_item_markup);


var panel_wip_items = new Ext.Panel({
	layout: 'border', height: 400,
	items: [ grid_wip_items, { id: 'work_item_detail', bodyStyle: { background: '#ffffff', padding: '7px' }, region: 'center', html: 'Please select a WIP Item to see more details', autoScroll: true } ]
});

grid_wip_items.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
		var wipPanel = Ext.getCmp('work_item_detail');
		wipItemTpl.overwrite(wipPanel.body, r.data);
});


center_panel.items = [ panel_wip_items ];
	
