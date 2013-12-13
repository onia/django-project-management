Ext.QuickTips.init();

/* Some constants used in forms and grids */
var GRID_HEIGHT = 550
var GRID_WIDTH = 500
var TEXTAREA_WIDTH = 400
var TEXTAREA_HEIGHT = 80 

/* 
 * Some reusable functions
 *
 */

var dateValue = "";

var st_users = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: "/Rota/Users/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk", mapping: "pk"},{name:"username", mapping: "extras.get_full_name"}]})
//	autoLoad: true
});

var st_rota_activities = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: "/Rota/RotaActivities/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk", mapping: "pk"},{name:"activity", mapping: "fields.activity"}]}),
	autoLoad: true
});

var st_rota_items = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: rota_url + dateValue }),
	reader: new Ext.data.JsonReader({ root: "", fields: [
		{name:"pk", mapping: "pk"},
		{name:"user", mapping: "user"},
		{name:"monday_date", mapping: "monday_date"},
		{name:"monday", mapping: "1_s"},
		{name:"monday_rota", mapping: "1_r"},
		{name:"monday_rota_desc", mapping: "1_r_d"},
		{name:"monday_engineering_days", mapping: "1_eday"},
		{name:"tuesday", mapping: "2_s"},
		{name:"tuesday_rota", mapping: "2_r"},
		{name:"tuesday_rota_desc", mapping: "2_r_d"},
		{name:"tuesday_engineering_days", mapping: "2_eday"},
		{name:"wednesday", mapping: "3_s"},
		{name:"wednesday_rota", mapping: "3_r"},
		{name:"wednesday_rota_desc", mapping: "3_r_d"},
		{name:"wednesday_engineering_days", mapping: "3_eday"},
		{name:"thursday", mapping: "4_s"},
		{name:"thursday_rota", mapping: "4_r"},
		{name:"thursday_rota_desc", mapping: "4_r_d"},
		{name:"thursday_engineering_days", mapping: "4_eday"},
		{name:"friday", mapping: "5_s"},
		{name:"friday_rota", mapping: "5_r"},
		{name:"friday_rota_desc", mapping: "5_r_d"},
		{name:"friday_engineering_days", mapping: "5_eday"},
		{name:"saturday", mapping: "6_s"},
		{name:"saturday_rota", mapping: "6_r"},
		{name:"saturday_rota_desc", mapping: "6_r_d"},
		{name:"saturday_engineering_days", mapping: "6_eday"},
		{name:"sunday", mapping: "7_s"},
		{name:"sunday_rota", mapping: "7_r"},
		{name:"sunday_rota_desc", mapping: "7_r_d"},
		{name:"sunday_engineering_days", mapping: "7_eday"}
		]}),
	autoLoad: true
});

var editor = new Ext.ux.grid.RowEditor({
        saveText: 'Update'
    });
    
    
var grid_rota = new Ext.grid.GridPanel({
        store: st_rota_items,
        columns: [
            {header: "pk", dataIndex: 'pk', sortable: true, hidden: true},
            {header: "User", dataIndex: 'user', sortable: true},
            {header: "Monday", dataIndex: 'monday', sortable: true },
            {header: "Tuesday", dataIndex: 'tuesday', sortable: true},
            {header: "Wednesday", dataIndex: 'wednesday', sortable: true},
            {header: "Thursday", dataIndex: 'thursday', sortable: true},
            {header: "Friday", dataIndex: 'friday', sortable: true},
            {header: "Saturday", dataIndex: 'saturday', sortable: true},
            {header: "Sunday", dataIndex: 'sunday', sortable: true}],
        tbar: [{
        	xtype: "fieldset",
        	iconCls: "icon-user",
        	defaultType: "datefield",
        	labelAlign: "left",
        	items: [{
           		fieldLabel: 'Select Date',
           		name: 'rotadate',
           		id: 'rotadate',
          		width: 100,
           		listeners: {
           		select: function(picker,date_string){
           			var chosen_date = new Date(date_string);
           			var year = chosen_date.getFullYear();
           			var month = chosen_date.getMonth() + 1;
           			var day = chosen_date.getDate();
           		
           			st_rota_items.proxy = new Ext.data.HttpProxy({ url: rota_url + year + "/" + month + "/" + day + "/" }),
           			st_rota_items.load()
           				}
          		}
           }]
           
      }],
	sm: new Ext.grid.RowSelectionModel({singleSelect: true}),
	viewConfig: { forceFit: true },
    height: GRID_HEIGHT,
    id:'grid_rota',
	region: "west",
	width: GRID_WIDTH,
	split: true
});

var markup_rota = [
	'<table class="project_table">',
	'<tr><td colspan="3"><h1>{user}</h1></td></tr>',
	'<tr><th>Day</th><th>Rota Activity</th><th>Notes</th><th>Engineering Days</th></tr>',
	'<tr><th>Monday</th> <td>{monday_rota}</td> <td>{monday_rota_desc}</td> <td>{monday_engineering_days}</td>					</tr>',
	'<tr><th>Tuesday</th> <td>{tuesday_rota}</td> <td>{tuesday_rota_desc}</td> <td>{tuesday_engineering_days}</td>				</tr>',
	'<tr><th>Wednesday</th> <td>{wednesday_rota}</td> <td>{wednesday_rota_desc}</td> <td>{wednesday_engineering_days}</td>			</tr>',
	'<tr><th>Thursday</th> <td>{thursday_rota}</td>	<td>{thursday_rota_desc}</td> <td>{thursday_engineering_days}</td>			</tr>',
	'<tr><th>Friday</th> <td>{friday_rota}</td> <td>{friday_rota_desc}</td> <td>{friday_engineering_days}</td>					</tr>',
	'<tr><th>Saturday</th> <td>{saturday_rota}</td>	 <td>{saturday_rota_desc}</td> <td>{saturday_engineering_days}</td>			</tr>',
	'<tr><th>Sunday</th> <td>{sunday_rota}</td> <td>{sunday_rota_desc}</td> <td>{sunday_engineering_days}</td>					</tr>',
	'</table>' ]
var template_rota = new Ext.Template(markup_rota);

var panel_rota = new Ext.Panel({
	layout: 'border', height: GRID_HEIGHT,
	items: [ grid_rota, { id: "rota_detail", bodyStyle: { background: "#ffffff", padding: "7px;"}, region: "center", html: "Please select a person to view more details", autoScroll: true, autoWidth: true } ]
});

var rota_fields = [
	{ xtype: "combo", fieldLabel: "Monday", hiddenName: "monday", lazyInit: false, store: st_rota_activities, mode: "local", displayField: "activity", valueField: "pk", triggerAction: "all", editable: false },
	{ xtype: "textfield", fieldLabel: "Description", name: "monday_description" },
	{ xtype: "combo", fieldLabel: "Tuesday", hiddenName: "tuesday", lazyInit: false, store: st_rota_activities, mode: "local", displayField: "activity", valueField: "pk", triggerAction: "all", editable: false },
	{ xtype: "textfield", fieldLabel: "Description", name: "tuesday_description" },
	{ xtype: "combo", fieldLabel: "Wednesday", hiddenName: "wednesday", lazyInit: false, store: st_rota_activities, mode: "local", displayField: "activity", valueField: "pk", triggerAction: "all", editable: false },
	{ xtype: "textfield", fieldLabel: "Description", name: "wednesday_description" },
	{ xtype: "combo", fieldLabel: "Thursday", hiddenName: "thursday", lazyInit: false, store: st_rota_activities, mode: "local", displayField: "activity", valueField: "pk", triggerAction: "all", editable: false },
	{ xtype: "textfield", fieldLabel: "Description", name: "thursday_description" },
	{ xtype: "combo", fieldLabel: "Friday", hiddenName: "friday", lazyInit: false, store: st_rota_activities, mode: "local", displayField: "activity", valueField: "pk", triggerAction: "all", editable: false },
	{ xtype: "textfield", fieldLabel: "Description", name: "friday_description" },
	{ xtype: "combo", fieldLabel: "Saturday", hiddenName: "saturday", lazyInit: false, store: st_rota_activities, mode: "local", displayField: "activity", valueField: "pk", triggerAction: "all", editable: false },
	{ xtype: "textfield", fieldLabel: "Description", name: "saturday_description" },
	{ xtype: "combo", fieldLabel: "Sunday", hiddenName: "sunday", lazyInit: false, store: st_rota_activities, mode: "local", displayField: "activity", valueField: "pk", triggerAction: "all", editable: false },
	{ xtype: "textfield", fieldLabel: "Description", name: "sunday_description" }
]
	

grid_rota.on('rowdblclick', function(sm, rowIdx, r) { 
	var person_id = grid_rota.getSelectionModel().getSelected().get("pk");
	var monday_date = grid_rota.getSelectionModel().getSelected().get("monday_date");
	var form_edit_rota = new Ext.form.FormPanel({ url: "/Rota/Edit/", bodyStyle: "padding: 15px;", autoScroll: true, items: rota_fields });
	form_edit_rota.getForm().load({ url: "/Rota/GetRotaFor/" + person_id + "/" + monday_date + "/", method: "GET" });
	var window_rota = new Ext.Window({ width: 620, autoHeight: true, closeAction: "close", autoScroll: true, modal: true, title: "Edit Rota", items: [ form_edit_rota ],
		buttons: [ {	text: 'Save', 
						handler: function(){
							form_edit_rota.getForm().submit({
								params: { monday_date: monday_date, person_id: person_id },
								success: function(f,a){
									Ext.message.msg('Success', 'Rota Updated', 5);
											window_rota.destroy();
											Ext.getCmp('grid_rota').store.load();
											Ext.getCmp('rota_detail').body.update('Please select a person to see more details');
								},
								failure: function(f,a){ Ext.Msg.alert('Warning', a.result.errormsg); }
							});
						}
				}, { text: 'Close', handler: function(){ window_rota.destroy(); } }]
				
	});	

	window_rota.show();
	window_rota.center();
	

});

grid_rota.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
	var detailRota = Ext.getCmp("rota_detail");
	template_rota.overwrite(detailRota.body, r.data);
});	


tab_items = [
	{ xtype: "panel", title: "Rota", items: [ panel_rota ] }
	]

var tabpanel = new Ext.TabPanel({ items: tab_items, bodyStyle: "padding: 15px;", activeTab: 0});	
center_panel.items = [ panel_rota ]
