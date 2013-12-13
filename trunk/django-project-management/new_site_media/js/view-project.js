Ext.QuickTips.init();

/* Some constants used in forms and grids */
var GRID_HEIGHT = 210;
var GRID_WIDTH = 500;
var TEXTAREA_WIDTH = 400;
var TEXTAREA_HEIGHT = 80;
var JSON_DATE = "Y-m-d h:i:s";
var DATE_RENDERER = Ext.util.Format.dateRenderer("d/m/Y");

/* 
 * Some reusable functions
 *
 */


var st_users = new Ext.data.Store({
    proxy: new Ext.data.HttpProxy({ url: "/xhr/" + project_number + "/get_users/" }),
    reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk", mapping: "pk"},{name:"username", mapping: "extras.get_full_name"}]}),
    autoLoad: true
});

var st_managers = new Ext.data.Store({
    proxy: new Ext.data.HttpProxy({ url: "/xhr/" + project_number + "/get_team_managers/" }),
    reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk", mapping: "pk"},{name:"username", mapping: "extras.get_full_name"}]}),
    autoLoad: true
});

var st_non_managers = new Ext.data.Store({
    proxy: new Ext.data.HttpProxy({ url: "/xhr/" + project_number + "/get_non_team_managers/" }),
    reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk", mapping: "pk"},{name:"username", mapping: "extras.get_full_name"}]}),
    autoLoad: true
});

var date_renderer = Ext.util.Format.dateRenderer('d/m/Y');

/* 
 *
 * DELIVERABLES!!!!
 *
 * */

var deliverable_fields = [
    { xtype: "textarea", fieldLabel: "Description", name: "description", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "deliverable-description" },
    { xtype: "textarea", fieldLabel: "Acceptance Criteria", name: "acceptance_criteria", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "deliverable-acceptance" },
    { xtype: "textfield", fieldLabel: "Deliverable Tester", name: "deliverable_tester", ttEnabled: true, cmsSlug: "deliverable-tester" },
    { xtype: "textarea", fieldLabel: "Method", name: "testing_method", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "deliverable-testing" },
    { xtype: "textarea", fieldLabel: "Expected Result", name: "expected_result", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "deliverable-result" },
    { xtype: "textfield", fieldLabel: "RPO", name: "rpo", ttEnabled: true, cmsSlug: "deliverable-rpo" },
    { xtype: "textfield", fieldLabel: "RTO", name: "rto", ttEnabled: true, cmsSlug: "deliverable-rto" } 
];

// Add a Deliverable
var add_deliverable = function(b,e){
    var form_add_deliverable = new Ext.form.FormPanel({ url: "/Deliverables/" + project_number + "/Add/", bodyStyle: "padding: 15px;", autoScroll: true, items: deliverable_fields });

    var window_deliverable = new Ext.Window({height: 540, width:620, closeAction: "hide", autoScroll: true, modal: true, title: "Add a Deliverable", items: [ form_add_deliverable ],
        buttons: [{ text:'Submit', 
            handler: function(){
                form_add_deliverable.getForm().submit({
                    success: function(f,a){
                        Ext.message.msg('Success', 'Deliverable Added', 5);
                        window_deliverable.hide(); 
                        Ext.getCmp("grid_deliverables").store.load();
                        Ext.getCmp("deliverable_detail").body.update('Please select a deliverable to see more details');
                    },  
                    failure: function(f,a){
                        Ext.Msg.alert('Warning', a.result.errormsg);
                    }
                });
            }},
            { text: 'Close', handler: function(){ window_deliverable.hide(); } }] });
    tabpanel.activate(1);
    window_deliverable.show();
    window_deliverable.center();
};

// Edit Deliverable
var edit_deliverable = function(b,e){

    var deliverable_id = grid_deliverables.getSelectionModel().getSelected().get("pk");
    var form_deliverable_edit = new Ext.form.FormPanel({url: "/Deliverables/" + project_number + "/" + deliverable_id + "/Edit/", bodyStyle: "padding: 15px;", autoScroll: true, items: deliverable_fields });
    form_deliverable_edit.getForm().load({ url: "/Deliverables/" + project_number + "/" + deliverable_id + "/", method: "GET" });
    var window_deliverable = new Ext.Window({width: 620, height:540, closeAction: "hide", autoScroll: true, modal: true, title: "Edit a Deliverable", items: [ form_deliverable_edit ],
        buttons: [ { text: 'Save',
            handler: function(){
                form_deliverable_edit.getForm().submit({
                    success: function(f,a){
                        window_deliverable.hide(); 
                        Ext.getCmp("grid_deliverables").store.load();
                        Ext.getCmp("deliverable_detail").body.update('Please select a deliverable to see more details');
                        Ext.message.msg('Success', 'Deliverable Updated', 5);
                    },  
                    failure: function(f,a){
                        Ext.Msg.alert('Warning', a.result.errormsg);
                    }
                });
            }} ,  
                { text: 'Close', handler: function(){ window_deliverable.hide(); } }] });
    window_deliverable.show();
    window_deliverable.center();
};

// Delete Deliverable
function delete_deliverable() {
    var deliverableId = grid_deliverables.getSelectionModel().getSelected().get("pk");
    var sm = grid_deliverables.getSelectionModel();
    var sel = sm.getSelected();
    if (sm.hasSelection()){
        Ext.Msg.show({
            title: 'Remove Deliverable',
            buttons: Ext.MessageBox.YESNO,
            msg: 'Remove <b>'+sel.data.description+'</b>?',
            closable: false, 
            fn: function(btn){
                if (btn == 'yes'){
                    Ext.Ajax.request({
                        url: "/Deliverables/" + project_number + "/" + deliverableId + "/" + "Delete/",
                        method: "POST", params: {"pk": deliverableId },
                        failure: function (response) {
                            Ext.Msg.alert('Error', response.responseText);
                        },
                        success: function (response) {
                            Ext.message.msg('Success', sel.data.description + " has been removed", 5);
                            Ext.getCmp("grid_deliverables").store.load();
                            Ext.getCmp("deliverable_detail").body.update('Please select a deliverable to see more details');
                        }
                    });
                }
            }
        });
    }
}
 
// Show Deliverables... 
var st_deliverable = new Ext.data.Store({
    proxy: new Ext.data.HttpProxy({ url: "/Deliverables/" + project_number + "/" }),
    reader: new Ext.data.JsonReader({ root: "", fields: [
        {name:"description", mapping: "fields.description"},
        {name:"pk", mapping: "pk"},
        {name:"acceptance_criteria", mapping: "fields.acceptance_criteria"},
        {name:"deliverable_tester",mapping:"fields.deliverable_tester"},
        {name:"testing_method", mapping: "fields.testing_method"},
        {name:"expected_result", mapping: "fields.expected_result"},
        {name:"rpo", mapping: "fields.rpo"},
        {name:"rto", mapping: "fields.rto"},
        {name:"created_date", type: "date", dateFormat: JSON_DATE, mapping: "fields.created_date"},
        {name:"modified_date", type: "date", dateFormat: JSON_DATE, mapping: "fields.modified_date"} ]}),
    autoLoad: true
});

var btn_update_deliverable = { iconCls: 'icon-update', text: 'Update Deliverable', handler: edit_deliverable };
var btn_delete_deliverable = { iconCls: 'icon-complete', text: 'Delete Deliverable', handler: delete_deliverable };

var grid_deliverables = new Ext.grid.GridPanel({
    store: st_deliverable,
    columns: [
        {header: "Description", dataIndex: 'description', sortable: true},
        {header: "Acceptance Criteria", dataIndex: 'acceptance_criteria', sortable: true},
        {header: "Tester", dataIndex: 'deliverable_tester', sortable: true},
        {header: "Method", dataIndex: 'testing_method', sortable: true, hidden: true},
        {header: "Expected Result", dataIndex: 'expected_result', sortable: true, hidden: true},
        {header: "RTO", dataIndex: 'rto', sortable: true, hidden: true },
        {header: "RPO", dataIndex: 'rpo', sortable: true, hidden: true },
        {header: "Created Date", dataIndex: 'created_date', sortable: true, hidden: true, renderer: DATE_RENDERER },
        {header: "Modified Date", dataIndex: 'modified_date', sortable: true, hidden: true, renderer: DATE_RENDERER } ],
    tbar: [ btn_update_deliverable, btn_delete_deliverable ],
    sm: new Ext.grid.RowSelectionModel({singleSelect: true}),
    viewConfig: { forceFit: true },
    height: GRID_HEIGHT,
    id:'grid_deliverables',
    width: GRID_WIDTH,
    split: true,
    region: 'west'
});

grid_deliverables.on('dblclick', function(){ edit_deliverable() });

var markup_deliverables = [
    '<table class="project_table">',
    '<tr><th>Description</th> <td>{description}</td></tr>',
    '<tr><th>Deliverable Tester</th> <td>{deliverable_tester}</td></tr>',
    '<tr><th>Acceptance Criteria</th> <td>{acceptance_criteria}</td></tr>',
    '<tr><th>Method</th> <td>{testing_method}</td></tr>',
    '<tr><th>Expected Result</th> <td>{expected_result}</td></tr>',
    '<tr><th>RPO</th> <td>{rpo}</td></tr>',
    '<tr><th>RTO</th> <td>{rto}</td></tr>',
    '<tr><th>Created Date</th> <td>{created_date}</td></tr>',
    '<tr><th>Modified Date</th> <td>{modified_date}</td></tr>', '</table>' ];
var template_deliverables = new Ext.Template(markup_deliverables);

var panel_deliverables = new Ext.Panel({
    layout: 'border', height: 400,
    items: [ grid_deliverables, { id: 'deliverable_detail', bodyStyle: { background: '#ffffff', padding: '7px' }, region: 'center', html: 'Please select a deliverable to see more details'} ]
});

grid_deliverables.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
    var detailPanel = Ext.getCmp('deliverable_detail');
    template_deliverables.overwrite(detailPanel.body, r.data);
});

/*
 *
 * RISKS!!!
 *
 * */
probability_list = ["", "Very Unlikely", "Unlikely", "Possible", "Likely"];
impact_list = ["", "Low Impact", "Some Impact", "High Impact", "Critical"];
var probability_tip = new Ext.ux.SliderTip({ getText: function(slider){ return String.format('<b>{0}</b>', probability_list[slider.getValue()]); } }); 
var impact_tip = new Ext.ux.SliderTip({ getText: function(slider){ return String.format('<b>{0}</b>', impact_list[slider.getValue()]); } }); 

var st_counter = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[1,"Prevention"],[2,"Acceptance"],[3,"Transfer"],[4,"Reduction"],[5,"Contingency"]]});
var st_status = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[1,"Closed"],[2,"Reducing"],[3,"Increasing"],[4,"No Change"]]});

var risk_fields = [
    { xtype: "textarea", fieldLabel: "Description", name: "description", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "risk-description" },
    { xtype: "combo", fieldLabel: "Owner", hiddenName: "owner", lazyInit: false, store: st_users, mode: "local", displayField: "username", valueField: "pk", triggerAction: "all", ttEnabled: true, cmsSlug: "risk-owner", editable: false },
    { xtype: "slider", minValue: 1, maxValue: 4, plugins: probability_tip, fieldLabel: "Probability", name: "probability", id: "probability", ttEnabled: true, cmsSlug: "risk-probability", listeners: {    
        change : function(slider, newValue) { getRating(); },
        setValue: function(slider) { slider.getValue(); }
        }
    },
    { xtype: "slider", minValue: 1, maxValue: 4, plugins: impact_tip, fieldLabel: "Impact", name: "impact", id: 'impact',  ttEnabled: true, cmsSlug: "risk-impact", listeners: {    
        change : function(slider, newValue) { getRating(); }
        }
    },
    { xtype: "textfield", fieldLabel: "Rating", name: "rating", readOnly: true, allowBlank: true, id:'rating', valueField:"rating", ttEnabled: true, cmsSlug: "risk-rating" },
    { xtype: "combo", displayField: "d", valueField: "id", hiddenName: 'counter_measure', mode: "local", store: st_counter, fieldLabel: "Counter Measure", name: "counter_measure", triggerAction: "all", ttEnabled: true, cmsSlug: "risk-countermeasure", editable: false },
    { xtype: "combo", displayField: "d", valueField: "id", hiddenName: 'status', mode: "local", store: st_status, fieldLabel: "Status", name: "status", triggerAction: "all", ttEnabled: true, cmsSlug: "risk-status", editable: false },
    { xtype: "textarea", fieldLabel: "Update", name: "update", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "risk-update" },
    { xtype: "textarea", fieldLabel: "History", name: "history", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, readOnly: true, ttEnabled: true, cmsSlug: "risk-history" }
];

function getRating() {
    Ext.getCmp("rating").setValue(((Ext.getCmp("probability").value * Ext.getCmp("impact").value) / 2));
}


var add_risk = function(b,e){

    var form_risk_add = new Ext.form.FormPanel({ url: "/Risks/" + project_number + "/Add/", bodyStyle: "padding: 15px;", autoScroll: true, items: risk_fields});

    var window_risks = new Ext.Window({ width: 620, height:540, closeAction:'close', autoScroll: true, modal: true, title: "Add a Risk", items: [ form_risk_add ],
        buttons: [{ text: 'Save',
            handler: function(){
                form_risk_add.getForm().submit({
                    params: { probability: Ext.getCmp("probability").getValue(), impact: Ext.getCmp("impact").getValue()  },
                    success: function(f,a){
                        Ext.message.msg('Success', 'Risk Added', 5); 
                        window_risks.destroy(); 
                        Ext.getCmp("grid_risks").store.load();
                        Ext.getCmp("risk_detail").body.update('Please select a risk to see more details');
                    },  
                    failure: function(f,a){
                        Ext.Msg.alert('Warning', a.result.errormsg);
                    }
                });
            }},
            { text: 'Close', handler: function(){ window_risks.destroy(); } }]
    });
    project_menu.hide();
    tabpanel.activate(2);
    window_risks.show();
    window_risks.center();
};

var edit_risk = function(b,e){
    var risk_id = grid_risks.getSelectionModel().getSelected().get("pk");
    var form_risk_edit = new Ext.form.FormPanel({ 
        url: "/Risks/" + project_number + "/" + risk_id + "/Edit/", bodyStyle: "padding: 15px;", 
        id: "form_risk_edit",
        autoScroll: true, items: risk_fields
    });
    form_risk_edit.getForm().load({ url: "/Risks/" + project_number + "/" + risk_id + "/", method: "GET" });
    var window_risks = new Ext.Window({width: 620, autoHeight: true, closeAction: "close", autoScroll: true, modal: true, title: "Edit Risk", items: [ form_risk_edit ],
        listeners: {
            activate: function(){
                var impactVal = grid_risks.getSelectionModel().getSelected().get("impact"); 
                var probabilityVal = grid_risks.getSelectionModel().getSelected().get("probability"); 
                Ext.getCmp("impact").setValue( impactVal, false);
                Ext.getCmp("probability").setValue( probabilityVal, false);
            }
        },
        buttons: [ { text: 'Save',
            handler: function(){
                form_risk_edit.getForm().submit({
                    params: { probability: Ext.getCmp("probability").getValue(), impact: Ext.getCmp("impact").getValue()  },
                        success: function(f,a){
                            Ext.message.msg('Success', 'Risk Updated', 5);
                            window_risks.destroy(); 
                            Ext.getCmp("grid_risks").store.load();
                            Ext.getCmp("risk_detail").body.update('Please select a risk to see more details');
                        },  
                        failure: function(f,a){
                            Ext.Msg.alert('Warning', a.result.errormsg);
                        }
                });
            }},   
            { text: 'Close', handler: function(){ window_risks.destroy(); } }] });
    window_risks.show();
    window_risks.center();
};

// Delete Risk
function delete_risk() {
    var riskId = grid_risks.getSelectionModel().getSelected().get("pk");
    var sm = grid_risks.getSelectionModel();
    var sel = sm.getSelected();
    if (sm.hasSelection()){
        Ext.Msg.show({
            title: 'Remove Risk',
            buttons: Ext.MessageBox.YESNO,
            msg: 'Remove <b>'+sel.data.risk_number+'</b>?',
            closable: false, 
            fn: function(btn){
                if (btn == 'yes'){
                    Ext.Ajax.request({
                        url: "/Risks/" + project_number + "/" + riskId + "/" + "Delete/",
                        method: "POST", params: {"pk": riskId },
                        failure: function (response) {
                            Ext.Msg.alert('Error', response.responseText);
                        },
                        success: function(result, request) { 
                            var res = new Object();
                            res = Ext.util.JSON.decode(result.responseText);
                            if (res.success == true) {
                                Ext.message.msg('Success', sel.data.risk_number + " has been removed", 5); 
                                Ext.getCmp("grid_risks").store.load();
                                Ext.getCmp("risk_detail").body.update('Please select a risk to see more details');
                            } else {
                                Ext.Msg.alert('Error', res.errormsg, 
                                function() { 
                                    Ext.getCmp("grid_risks").store.load();
                                    Ext.getCmp("risk_detail").body.update('Please select a risk to see more details');
                                });
                            }
                        }
                    });
                }
            }
        });
    }
}


var st_risks = new Ext.data.Store({
    proxy: new Ext.data.HttpProxy({ url: "/Risks/" + project_number + "/" }),
    reader: new Ext.data.JsonReader({ root: "", fields: [   
        {name:"pk", mapping: "pk"},
        { name: "risk_number", mapping: "fields.risk_number" },
        { name: "created_date", mapping: "fields.created_date", type: "date", dateFormat: JSON_DATE },	
        { name: "modified_date", mapping: "fields.modified_date", type: "date", dateFormat: JSON_DATE },	
        { name: "description", mapping: "fields.description" },	
        { name: "owner", mapping: "fields.owner.extras.get_full_name" },	
        { name: "probability", mapping: "fields.probability" },	
        { name: "impact", mapping: "fields.impact" },	
        { name: "rating", mapping: "fields.rating" },	
        { name: "history", mapping: "fields.history" },	
        { name: "history_html", mapping: "extras.get_history_html" },	
        { name: "counter_measure", mapping: "fields.counter_measure" },	
        { name: "status", mapping: "fields.status" }	]	}),
    autoLoad: true
});

var btn_update_risk = { iconCls: 'icon-update', text: 'Update Risk', handler: edit_risk };
var btn_delete_risk = { iconCls: 'icon-complete', text: 'Delete Risk', handler: delete_risk };

var grid_risks = new Ext.grid.GridPanel({
    store: st_risks,
    columns: [
        {header: "Risk Number", dataIndex: 'risk_number'},
        {header: "Description", dataIndex: 'description'},
        {header: "Probability", dataIndex: 'probability'},
        {header: "Impact", dataIndex: 'impact'},
        {header: "Created Date", dataIndex: 'created_date', sortable: true, hidden: true, renderer: DATE_RENDERER },
        {header: "Modified Date", dataIndex: 'modified_date', sortable: true, hidden: true, renderer: DATE_RENDERER },
        {header: "Rating", dataIndex: 'rating'} ],
    sm: new Ext.grid.RowSelectionModel({singleSelect: true}),
    viewConfig: { forceFit: true },
    tbar: [ btn_update_risk, btn_delete_risk ],
    height: GRID_HEIGHT,
    id:'grid_risks',
    width: GRID_WIDTH,
    split: true,
    region: 'west'
});

grid_risks.on('dblclick', function(){ edit_risk() });

var riskMarkup = [
    '<table class="project_table">',
    '<tr><th>Risk Number</th> <td>{risk_number}</td></tr>',
    '<tr><th>Description</th> <td>{description}</td></tr>',
    '<tr><th>Owner</th> <td>{owner}</td></tr>',
    '<tr><th>Probability</th> <td>{probability}</td></tr>',
    '<tr><th>Impact</th> <td>{impact}</td></tr>',
    '<tr><th>Rating</th> <td>{rating}</td></tr>',
    '<tr><th>Counter Measure</th> <td>{counter_measure}</td></tr>',
    '<tr><th>Status</th> <td>{status}</td></tr>',
    '<tr><th>History</th> <td>{history_html}</td></tr>',
    '<tr><th>Created Date</th> <td>{created_date}</td></tr>',
    '<tr><th>Modified Date</th> <td>{modified_date}</td></tr>', '</table>' ];
var riskTpl = new Ext.Template(riskMarkup);

var risk_panel = new Ext.Panel({
    layout: 'border', height: 400,
    items: [ grid_risks, { id: 'risk_detail', bodyStyle: { background: '#ffffff', padding: '7px' }, region: 'center', html: 'Please select a Risk to see more details'} ]
});

grid_risks.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
    var riskPanel = Ext.getCmp('risk_detail');
    riskTpl.overwrite(riskPanel.body, r.data);
});

/*
 * Create the WBS Grid 
 */
var st_skillset = new Ext.data.Store({
    proxy: new Ext.data.HttpProxy({ url: "/xhr/" + project_number + "/get_skillset/" }),
    reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk",mapping:"pk"},{name:"skill",mapping:"fields.skill"}]}),
    autoLoad: true
});


// Stage Plan
var st_stage_plan = new Ext.data.Store({
    proxy: new Ext.data.HttpProxy({ url: "/WBS/" + project_number + "/StagePlan/" }),
    reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk",mapping:"pk"},{name:"stage",mapping:"fields.stage"},{name:"description",mapping:"fields.description"},{name:"stage_number",mapping:"fields.stage_number"}]}),
    autoLoad: true,
    id: "st_stage_plan"
});


var percentage_tip = new Ext.ux.SliderTip({ getText: function(slider){ return slider.value } }); 

var st_wbs = new Ext.data.GroupingStore({
    proxy: new Ext.data.HttpProxy({ url: "/WBS/" + project_number + "/" }),
    reader: new Ext.data.JsonReader({ root: "", 
    fields: [
        { name: "pk", mapping: "pk" },
        { name: "created_date", mapping: "fields.created_date", type: "date", dateFormat: JSON_DATE },
        { name: "modified_date", mapping: "fields.modified_date", type: "date", dateFormat: JSON_DATE },
        { name: "skill_set", mapping: "fields.skill_set.fields.skill" },
        { name: "project_stage", mapping: "fields.project_stage.fields.stage" },
        { name: "author", mapping: "fields.author.extras.get_full_name" },
        { name: "title", mapping: "fields.title" },
        { name: "depends", mapping: "fields.depends.fields.title" },
        { name: "description", mapping: "fields.description" },
        { name: "duration", mapping: "fields.duration" },
        { name: "owner", mapping: "fields.owner.extras.get_full_name" },
        { name: "percent_complete", mapping: "fields.percent_complete" },
        { name: "start_date", mapping: "fields.start_date", type: "date", dateFormat: JSON_DATE },
        { name: "finish_date", mapping: "fields.finish_date", type: "date", dateFormat: JSON_DATE },
        { name: "wbs_number", mapping: "fields.wbs_number" },
        { name: "cost", mapping: "fields.cost" },
        { name: "history", mapping: "fields.history" },
        { name: "history_html", mapping: "extras.get_history_html" },
        { name: "engineering_days", mapping: "fields.engineering_days" },
        { name: "get_work_item_status", mapping: "fields.get_work_item_status" }
    ]}),
    autoLoad: true,
    groupField: 'project_stage',
    sortInfo:{field: 'wbs_number', direction: "ASC"}
});



var wbs_fields = [ 
    { xtype: "combo", fieldLabel: "Skill Set", name: "skill_set", hiddenName: "skill_set", lazyInit: false, store: st_skillset, mode: "local", displayField: "skill", valueField: "pk", triggerAction: "all", ttEnabled: true, cmsSlug: "wbs-skillset", editable: false },
    { xtype: "textfield", fieldLabel: "Title", name: "title", ttEnabled: true, cmsSlug: "wbs-title" },
    { xtype: "combo", fieldLabel: "Project Stage", hiddenName: "project_stage", lazyInit: false, store: st_stage_plan, mode: "local", displayField: "stage", valueField: "pk", triggerAction: "all", ttEnabled: true, cmsSlug: "wbs-stage", editable: false, allowBlank: false },
    { xtype: "combo", fieldLabel: "Depends Upon", hiddenName: "depends", lazyInit: false, store: st_wbs, mode: "local", displayField: "title", valueField: "pk", triggerAction: "all", ttEnabled: true, cmsSlug: "wbs-depends", editable: false },
    { xtype: "textarea", fieldLabel: "Description", name: "description", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "wbs-description" },
    { xtype: "textfield", fieldLabel: "Duration", name: "duration", ttEnabled: true, cmsSlug: "wbs-duration" },
    { xtype: "combo", fieldLabel: "Owner", hiddenName: "owner", lazyInit: false, store: st_users, mode: "local", displayField: "username", valueField: "pk", triggerAction: "all", ttEnabled: true, cmsSlug: "wbs-owner", editable: false },
    { xtype: "slider", minValue: 0, maxValue: 100, increment: 10, plugins: percentage_tip, fieldLabel: "Percentage Complete", name: "percent_complete", 
        id: "percent_complete",
        listeners: { setValue: function(slider) { slider.getValue(); } }  
    },
    { xtype: "datefield", fieldLabel: "Start Date", name: "start_date", format: "d/m/Y", ttEnabled: true, cmsSlug: "wbs-startdate" },
    { xtype: "datefield", fieldLabel: "Finish Date", name: "finish_date", format: "d/m/Y", ttEnabled: true, cmsSlug: "wbs-finishdate" },
    //	{ xtype: "textfield", fieldLabel: "WBS Number", name: "wbs_number" },
    { xtype: "textfield", fieldLabel: "Cost", name: "cost", ttEnabled: true, cmsSlug: "wbs-cost" },
    { xtype: "textarea", fieldLabel: "Update", name: "update", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "wbs-update" },
    { xtype: "textarea", fieldLabel: "History", name: "history", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, readOnly: true, ttEnabled: true, cmsSlug: "wbs-history" }
];

var stage_plan_fields = [
    { xtype: "numberfield", fieldLabel: "Stage Number", name: "stage_number", ttEnabled: true, cmsSlug: "wbs-stagenumber" },
    { xtype: "textfield", fieldLabel: "Stage", name: "stage", ttEnabled: true, cmsSlug: "wbs-stage" },
    { xtype: "textarea", fieldLabel: "Description", name: "description", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "wbs-stagedescription" }];

var add_wbs = function(b,e){
    var form_add_wbs = new Ext.form.FormPanel({ url: "/WBS/" + project_number + "/Add/", bodyStyle: "padding: 15px;", autoScroll: true, items: wbs_fields});
    var window_wbs = new Ext.Window({autoHeight: true, width:620, closeAction: "close", autoScroll: true, modal: true, title: "Add a Work Item", items: [ form_add_wbs ],
        buttons: [	{ 	text:'Submit', 
            handler: function(){
                form_add_wbs.getForm().submit({
                    params: { percent_complete: Ext.getCmp("percent_complete").getValue() },
                    success: function(f,a){
                        Ext.message.msg('Success', 'Work Item Added', 5);
                        window_wbs.destroy(); 
                        Ext.getCmp("grid_wbs").store.load();
                        Ext.getCmp("wbs_detail").body.update('Please select a Work Item to see more details');
                    },  
                    failure: function(f,a){
                        Ext.Msg.alert('Warning', a.result.errormsg);
                    }
                });
            }},
            { text: 'Close', handler: function(){ window_wbs.destroy(); } }] });
    window_wbs.show();
    window_wbs.center();
};

// Delete Work Item
var delete_wbs = function(b,e){
    var wbsId = grid_wbs.getSelectionModel().getSelected().get("pk");
    var sm = grid_wbs.getSelectionModel();
    var sel = sm.getSelected();
    if (sm.hasSelection()){
        Ext.Msg.show({
            title: 'Remove Work Item', buttons: Ext.MessageBox.YESNO,
            msg: 'Remove <b>'+sel.data.description+'</b>?', closable: false, 
            fn: function(btn){
                if (btn == 'yes'){
                    Ext.Ajax.request({
                        url: "/WBS/" + project_number + "/" + wbsId + "/Delete/",
                        method: "POST", params: {"pk": wbsId },
                        failure: function (response) {
                            Ext.Msg.alert('Error', response.responseText);
                        },
                        success: function (response) {
                            Ext.message.msg('Success', sel.data.description + " has been removed", 5);
                            Ext.getCmp("grid_wbs").store.load();
                            Ext.getCmp("wbs_detail").body.update('Please select a Work Item to see more details');
                        }
                    });
                }
            }
        });
    }
};


var edit_wbs = function(b,e){
    var	wbs_id = grid_wbs.getSelectionModel().getSelected().get("pk");
    var form_wbs_edit = new Ext.form.FormPanel({ 
        url: "/WBS/" + project_number + "/" + wbs_id + "/Edit/", bodyStyle: "padding: 15px;", id: "form_wbs_edit", autoScroll: true, items: wbs_fields });
    form_wbs_edit.getForm().load({ url: "/WBS/" + project_number + "/" + wbs_id + "/", method: "GET" });
    var window_wbs = new Ext.Window({width: 620, autoHeight: true, closeAction: "close", autoScroll: true, modal: true, title: "Edit Work Item", items: [ form_wbs_edit ],
        listeners: {
            activate: function(){
                var percentCompleteVal = grid_wbs.getSelectionModel().getSelected().get("percent_complete"); 
                Ext.getCmp("percent_complete").setValue( percentCompleteVal, false);
            }
        },
        buttons: [ { text: 'Save',
            handler: function(){
                form_wbs_edit.getForm().submit({
                    params: { percent_complete: Ext.getCmp("percent_complete").getValue() },
                    success: function(f,a){
                        Ext.message.msg('Success', 'Work Item Updated', 5);
                        window_wbs.destroy(); 
                        Ext.getCmp("grid_wbs").store.load();
                        Ext.getCmp("wbs_detail").body.update('Please select a Work Item to see more details');
                    }});
            }}]
    });
    window_wbs.show();
    window_wbs.center();
};
									    
									    
// Engineering Days
var st_engineering_day_resource =  new Ext.data.Store({
    reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk",mapping:"pk"},{name:"resource", mapping:"resource"},{name:"available", mapping:"available"}]})
});

var st_engineering_day_type = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[0,"Half-day AM"],[1,"Half-day PM"],[2,"Full Day"]]});

var get_resources_from_date = function(picker,date_string){
    var wbs_id = grid_wbs.getSelectionModel().getSelected().get("pk");
    var day_type = Ext.getCmp("eday_day_type").getValue();
    var chosen_date = new Date(date_string);
    var year = chosen_date.getFullYear();
    var month = chosen_date.getMonth() + 1;
    var day = chosen_date.getDate();
    st_engineering_day_resource.proxy = new Ext.data.HttpProxy({ url: "/WBS/" + project_number + "/EngineeringDayResources/" + year + "-" + month + "-" + day + "/" + wbs_id + "/" + day_type + "/"});
    st_engineering_day_resource.load();
}

var get_resources_from_day_type = function(){
    var wbs_id = grid_wbs.getSelectionModel().getSelected().get("pk");
    var day_type = Ext.getCmp("eday_day_type").getValue();
    var date_string = Ext.getCmp("eday_date").getValue();
    var chosen_date = new Date(date_string);
    var year = chosen_date.getFullYear();
    var month = chosen_date.getMonth() + 1;
    var day = chosen_date.getDate();
    st_engineering_day_resource.proxy = new Ext.data.HttpProxy({ url: "/WBS/" + project_number + "/EngineeringDayResources/" + year + "-" + month + "-" + day + "/" + wbs_id + "/" + day_type + "/"});
    st_engineering_day_resource.load();
}

var engineering_day_fields = [
    { xtype: "datefield", fieldLabel: "Date", format: 'd/m/Y', name: "work_date", listeners: { select: get_resources_from_date }, id: "eday_date", ttEnabled: true, cmsSlug: "engineering-day-date" },
    { xtype: "combo", fieldLabel: "Day Type", hiddenName: "day_type", lazyInit: false, store: st_engineering_day_type, mode: "local", displayField: "d", valueField: "id", triggerAction: "all", id: "eday_day_type", listeners: { select: get_resources_from_day_type}, ttEnabled: true, cmsSlug: "engineering-day-type", editable: false },
    { xtype: "combo", fieldLabel: "Resource", hiddenName: "resource", lazyInit: false, store: st_engineering_day_resource, mode: "local", displayField: "resource", valueField: "pk", triggerAction: "all", width: 300, ttEnabled: true, cmsSlug: "engineering-day-resource", editable: false  }
]

var add_engineering_day = function(){

    var wbs_id = grid_wbs.getSelectionModel().getSelected().get("pk");
    var form_add_engineering_day = new Ext.form.FormPanel({ url: "/WBS/" + project_number + "/AddEngineeringDay/" + wbs_id + "/", bodyStyle: "padding: 15px;", autoScroll: true, items: engineering_day_fields });	
    var window_engineering_day = new Ext.Window({ width: 620, autoHeight: true, closeAction: "close", autoScroll: true, modal: true, title: "Add Engineering Day", items: [ form_add_engineering_day ],
        buttons: [ { text: "Save",
            handler: function(){ 
                form_add_engineering_day.getForm().submit({
                    success: function(f,a){
                        Ext.message.msg('Success', 'Engineering Day Booked', 5);
                        window_engineering_day.close();
                        Ext.getCmp("grid_wip_items").store.load();
                        Ext.getCmp("wbs_detail").body.update('Please select a Work Item to see more details');
                    },
                    failure: function(f,a){
                        Ext.Msg.alert('Warning', a.result.errormsg);
                    }
                });
            }},
            { text: "Close", handler: function(){ window_engineering_day.close(); }} ]
    });
    window_engineering_day.show();
    window_engineering_day.center();
};
									    
var add_project_stage = function(b,e){
    var form_add_project_stage = new Ext.form.FormPanel({ url: "/WBS/" + project_number + "/StagePlan/Add/", bodyStyle: "padding: 15px;", autoScroll: true, items: stage_plan_fields });
    var window_stage_plan = new Ext.Window({ width: 620, height: 300, closeAction: "hide", autoScroll: true, modal: true, title: "Add a Project Stage", items: [ form_add_project_stage ],
        buttons: [	{ 	text:'Submit', 
            handler: function(){
                form_add_project_stage.getForm().submit({
                    success: function(f,a){
                        Ext.message.msg('Success', 'Project Stage Added', 5);
                        window_stage_plan.hide(); 
                        window.location.reload(); // At the moment we have to reload at this point - to be resolved.
                    },  
                    failure: function(f,a){
                        Ext.Msg.alert('Warning', a.result.errormsg);
                    }
                });
            }},
            { text: 'Close', handler: function(){ window_stage_plan.hide(); } }] });
    window_stage_plan.show();
    window_stage_plan.center();
};

var btn_add_wbs = { iconCls: 'icon-add', text: 'Add Work Item', handler: add_wbs }
var btn_update_wbs = { iconCls: 'icon-update', text: 'Update Work Item', handler: edit_wbs }
var btn_delete_wbs = { iconCls: 'icon-complete', text: 'Delete Work Item', handler: delete_wbs }
var btn_add_project_stage = { iconCls: 'icon-add', text: 'Add Project Stage', handler: add_project_stage }
var btn_add_engineering_day = { iconCls: 'icon-add', text: 'Add Engineering Day', handler: add_engineering_day }

var copyGridDataToString = function(grid) {
    var s = '';
    var rec = 0;
    grid.getSelectionModel().selectAll();
    var selRecords = grid.getSelectionModel().getSelections();
    for (rec = 0; rec < selRecords.length; rec++) {
        s += selRecords[rec].get('pk') + ',';
    }
    grid.getSelectionModel().clearSelections();
    return s;
}

var grid_wbs_dragdrop = new Ext.ux.dd.GridDragDropRowOrder({
    copy: false,
    scrollable: true,
    listeners: { afterrowmove: function(objThis, oldIndex, newIndex, records){
        var s = copyGridDataToString(grid_wbs);
        Ext.Ajax.request({
            url: "/WBS/" + project_number + "/Reorder/",
            method: "POST", params: {"work_item_order": s },
            failure: function(response){
                Ext.Msg.alert('Error', response.responseText);
            },
            success: function(response){
                Ext.message.msg('Success', 'Work Item reordered<br>Please be aware that the new WBS number will not show until you refresh the page', 5);
            }
        })
    }}

});

var grid_wbs = new Ext.grid.GridPanel({
    store: st_wbs,
    id: "grid_wbs",
    columns: [
        {header: "WBS Number", dataIndex: 'wbs_number', hidden: false, sortable: true },
        {header: "Skill Set", dataIndex: 'skill_set', hidden: true, sortable: true },
        {header: "Stage", dataIndex: 'project_stage'},
        {header: "Author", dataIndex: 'author', hidden: true, sortable: true },
        {header: "Title", dataIndex: 'title', sortable: true },
        {header: "Description", dataIndex: 'description', hidden: true },
        {header: "Duration", dataIndex: 'duration', hidden: true, sortable: true },
        {header: "Owner", dataIndex: 'owner', hidden: true, sortable: true },
        {header: "Percent Complete", dataIndex: 'percent_complete', sortable: true },
        {header: "Start Date", dataIndex: 'start_date', hidden: true, sortable: true, renderer: DATE_RENDERER },
        {header: "Finish Date", dataIndex: 'finish_date', hidden: true, sortable: true, renderer: DATE_RENDERER },
        {header: "Work Status", dataIndex: 'get_work_item_status', hidden: true, sortable: true },
        {header: "Cost", dataIndex: 'cost'},
        {header: "Created Date", dataIndex: 'created_date', hidden: true, sortable: true, renderer: DATE_RENDERER },
        {header: "Modified Date", dataIndex: 'modified_date', hidden: true, sortable: true, renderer: DATE_RENDERER }
    ],
    tbar: [ btn_add_project_stage, btn_add_wbs, btn_update_wbs, btn_delete_wbs, btn_add_engineering_day ],
    plugins: [ grid_wbs_dragdrop ],
    sm: new Ext.grid.RowSelectionModel({singleSelect: false}),
    view: new Ext.grid.GroupingView({
        forceFit:true,
        getRowClass: function(record, rowIndex, rp, ds){
            return record.json.extras.get_work_item_status;
        },
        onRowSelect: function(row){
            this.addRowClass(row, this.getRowClass(this.grid.getStore().getAt(row)) + '-selected');
        },
        onRowDeselect: function(row){
            this.removeRowClass(row, this.getRowClass(this.grid.getStore().getAt(row)) + '-selected');
        },
        onRowOver: function(e, t){
            var row;
            if((row = this.findRowIndex(t)) !== false){
                this.addRowClass(this.findRowIndex(t), this.getRowClass(this.grid.getStore().getAt(this.findRowIndex(t))) + '-hover');
                this.grid.fireEvent('rowmouseover', this.grid, row);
            }
        },
        onRowOut: function(e,t){
            var row;
            if((row = this.findRowIndex(t)) !== false && !e.within(this.getRow(row), true)){
                this.removeRowClass(this.findRowIndex(t), this.getRowClass(this.grid.getStore().getAt(this.findRowIndex(t))) + '-hover');
                this.grid.fireEvent('rowmouseout', this.grid, row);
            }
        },
        groupTextTpl: '{text} ({[values.rs.length]} {[values.rs.length > 1 ? "Items" : "Item"]})'
    }),
    height: GRID_HEIGHT,
    width: GRID_WIDTH,
    split: true,
    region: 'west'
});

grid_wbs.on('dblclick', function(){ edit_wbs() });

var markup_wbs = [
	'<table class="project_table">',
//	'<tr><th>WBS Number</th> <td>{wbs_number}</td></tr>',
	'<tr><th>Skillset</th> <td>{skill_set}</td></tr>',
	'<tr><th>Stage</th> <td>{project_stage}</td></tr>',
	'<tr><th>Title</th> <td>{title}</td></tr>',
	'<tr><th>Description</th> <td>{description}</td></tr>',
	'<tr><th>Author</th> <td>{author}</td></tr>',
	'<tr><th>Depends Upon</th> <td>{depends}</td></tr>',
	'<tr><th>Duration</th> <td>{duration}</td></tr>',
	'<tr><th>Owner</th> <td>{owner}</td></tr>',
	'<tr><th>Cost</th> <td>{cost}</td></tr>',
	'<tr><th>Percent Complete</th> <td>{percent_complete}%</td></tr>',
	'<tr><th>Start Date</th> <td>{start_date}</td></tr>',
	'<tr><th>Finish Date</th> <td>{finish_date}</td></tr>',
	'<tr><th>History</th> <td>{history_html}</td></tr>',
	'<tr><th>Created Date</th> <td>{created_date}</td></tr>',
	'<tr><th>Modified Date</th> <td>{modified_date}</td></tr>', '</table>' ];
var tpl_wbs = new Ext.Template(markup_wbs);

var panel_wbs = new Ext.Panel({
	layout: 'border', height: 400,
	items: [ grid_wbs, { id: 'wbs_detail', bodyStyle: { background: '#ffffff', padding: '7px' }, region: 'center', html: 'Please select a Work Item to see more details', autoScroll: true} ]
});

grid_wbs.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
		var panel_wbs = Ext.getCmp('wbs_detail');
		tpl_wbs.overwrite(panel_wbs.body, r.data);
});



/*
 *
 * Create the Issues Grid
 *
 */
var st_issue_type = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[1,"Request For Change"],[2,"Off Specifications"],[3,"Concern"],[4,"Question"]]});
var st_issue_status = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[1,"Open"],[2,"In Progress"],[3,"Completed"],[4,"Closed"]]});
var st_issue_priority = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[1,"1"],[2,"2"],[3,"3"],[4,"4"],[5,"5"]]});
var issue_fields = [
	{ xtype: "textarea", fieldLabel: "Description", name: "description", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "issue-description" },
	{ xtype: "combo", fieldLabel: "Owner", hiddenName: "owner", name: "owner", lazyInit: false, store: st_users, mode: "local", displayField: "username", valueField: "pk", triggerAction: "all", ttEnabled: true, cmsSlug: "issue-owner", editable: false },
	{ xtype: "combo", fieldLabel: "Type", hiddenName: "type", name: "type", lazyInit: false, store: st_issue_type, mode: "local", displayField: "d", valueField: "id", triggerAction: "all", ttEnabled: true, cmsSlug: "issue-type", editable: false },
	{ xtype: "combo", fieldLabel: "Status", hiddenName: "status", name: "status", lazyInit: false, store: st_issue_status, mode: "local", displayField: "d", valueField: "id", triggerAction: "all", ttEnabled: true, cmsSlug: "issue-status", editable: false },
	{ xtype: "combo", fieldLabel: "Priority", hiddenName: "priority", name: "priority", lazyInit: false, store: st_issue_priority, mode: "local", displayField: "d", valueField: "id", triggerAction: "all", ttEnabled: true, cmsSlug: "issue-priority", editable: false }, 
	{ xtype: "textfield", fieldLabel: "Related RFC", name: "related_rfc", ttEnabled: true, cmsSlug: "issue-related-rfc" },
	{ xtype: "textfield", fieldLabel: "Related Helpdesk", name: "related_helpdesk", ttEnabled: true, cmsSlug: "issue-related-helpdesk"  },
    { xtype: "textarea", fieldLabel: "Update", name: "update", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "issue-update" },
    { xtype: "textarea", fieldLabel: "History", name: "history", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, readOnly: true, ttEnabled: true, cmsSlug: "issue-history" }
];

var add_issue = function(b,e){
	var form_add_issue = new Ext.form.FormPanel({ url: "/Issues/" + project_number + "/Add/", bodyStyle: "padding: 15px;", autoScroll: true, items: issue_fields});
	var window_issues = new Ext.Window({width: 620, height:540, closeAction: "hide", autoScroll: true, modal: true, title: "Add a Issue", items: [ form_add_issue ],
							buttons: [	{ 	text:'Submit', 
											handler: function(){
												form_add_issue.getForm().submit({
													params: { author: user_id },
													success: function(f,a){
                                            		Ext.message.msg('Success', 'Issue Added', 5);
							window_issues.hide();
                                            		Ext.getCmp("issues_grid").store.load();
                                            		Ext.getCmp("issues_detail").body.update('Please select an issue to see more details');
                                            	},  
                                            		failure: function(f,a){
                                            		Ext.Msg.alert('Warning', a.result.errormsg);
													}
												});
										}} , { text: 'Close', handler: function(){ window_issue.hide(); } }] });
	project_menu.hide();
	tabpanel.activate(4);
	window_issues.show();
	window_issues.center();
};

var edit_issue = function(b,e){
	var	issue_id = grid_issues.getSelectionModel().getSelected().get("pk");
	var form_issue_edit = new Ext.form.FormPanel({ 
		url: "/Issues/" + project_number + "/" + issue_id + "/Edit/", bodyStyle: "padding: 15px;", 
		id: "form_issue_edit",
		autoScroll: true, items: issue_fields
		});
	form_issue_edit.getForm().load({ url: "/Issues/" + project_number + "/" + issue_id + "/", method: "GET" });
	var window_issues = new Ext.Window({width: 620, height:540, closeAction: "hide", autoScroll: true, modal: true, title: "Edit Issue", items: [ form_issue_edit ],
							buttons: [ { text: 'Save',
                                         handler: function(){
                                         form_issue_edit.getForm().submit({
                                            success: function(f,a){
                                            Ext.message.msg('Success', 'Issue Updated', 5);
                                            	window_issues.hide(); 
                                            	Ext.getCmp("issues_grid").store.load();
                                            	Ext.getCmp("issues_detail").body.update('Please select an issue to see more details');
									    },  
                                           	failure: function(f,a){
                                           Ext.Msg.alert('Warning', a.result.errormsg);
                                            }
                                        });
                                        }}   , { text: 'Close', handler: function(){ window_issues.hide(); } }] });
	window_issues.show();
	window_issues.center();

};


// Delete Issue
function delete_issue() {
	var issueId = grid_issues.getSelectionModel().getSelected().get("pk");
	var sm = grid_issues.getSelectionModel();
	var sel = sm.getSelected();
	if (sm.hasSelection()){
		Ext.Msg.show({
			title: 'Remove Issue',
			buttons: Ext.MessageBox.YESNO,
			msg: 'Remove <b>'+sel.data.description+'</b>?',
			closable: false, 
			fn: function(btn){
				if (btn == 'yes'){
						Ext.Ajax.request({
        url: "/Issues/" + project_number + "/" + issueId + "/Delete/",
        method: "POST",
        params: {"pk": issueId },
        failure: function (response) {
            Ext.Msg.alert('Error', response.responseText);
        },
        success: function(result, request) { 
                            var res = new Object();
                            res = Ext.util.JSON.decode(result.responseText);
                            
                             if (res.success == true)
                             {
                             	Ext.message.msg('Success', 'Issue Deleted', 5); 
                              	Ext.getCmp("issues_grid").store.load();
                               	Ext.getCmp("issues_detail").body.update('Please select an issue to see more details');
                            }
                            else {
                               Ext.Msg.alert('Error', res.errormsg, 
                           function() { 
                           	  	Ext.getCmp("issues_grid").store.load();
                               	Ext.getCmp("issues_detail").body.update('Please select an issue to see more details');
                                            	});
                             }
  						  }
 					 });
				}
			}
		});
	}
}


var st_issues = new Ext.data.GroupingStore({
	proxy: new Ext.data.HttpProxy({ url: "/Issues/" + project_number + "/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [
		{name:"pk", mapping: "pk"},
		{ name: "created_date", mapping: "fields.created_date", type: "date", dateFormat: JSON_DATE },
		{ name: "modified_date", mapping: "fields.modified_date", type: "date", dateFormat: JSON_DATE },
		{ name: "description", mapping: "fields.description" },
		{ name: "owner", mapping: "fields.owner.extras.get_full_name" },
		{ name: "author", mapping: "fields.author.extras.get_full_name" },
		{ name: "type", mapping: "fields.type" },
		{ name: "status", mapping: "fields.status" },
		{ name: "history", mapping: "fields.history" },
		{ name: "history_html", mapping: "extras.get_history_html" },
		{ name: "priority", mapping: "fields.priority" },
		{ name: "related_rfc", mapping: "fields.related_rfc" },
		{ name: "related_helpdesk", mapping: "fields.related_helpdesk" } ]}),
	autoLoad: true,
    groupField: 'type',
	sortInfo:{field: 'description', direction: "ASC"}
});

var btn_update_issues = { iconCls: 'icon-update', text: 'Update Issue', handler: edit_issue };
var btn_delete_issues = { iconCls: 'icon-complete', text: 'Delete Issue', handler: delete_issue };

var grid_issues = new Ext.grid.GridPanel({
	store: st_issues,
	columns: [
            {header: "Description", dataIndex: 'description'},
            {header: "Owner", dataIndex: 'owner', sortable: true},
            {header: "Created Date", dataIndex: 'created_date', hidden: true, sortable: true, renderer: DATE_RENDERER },
            {header: "Modified Date", dataIndex: 'modified_date', hidden: true, sortable: true, renderer: DATE_RENDERER },
            {header: "Author", dataIndex: 'author', hidden: true, sortable: true },
            {header: "Status", dataIndex: 'status', sortable: true },
            {header: "Type", dataIndex: 'type', sortable: true },
            {header: "Priority", dataIndex: 'priority' },
            {header: "Related RFC", dataIndex: 'related_rfc', hidden: true, sortable: true},
            {header: "Related Helpdesk", dataIndex: 'related_helpdesk', hidden: true, sortable: true}
	],
    tbar: [ btn_update_issues, btn_delete_issues ],
	sm: new Ext.grid.RowSelectionModel({singleSelect: true}),
	view: new Ext.grid.GroupingView({
		forceFit:true,
		groupTextTpl: '{text} ({[values.rs.length]} {[values.rs.length > 1 ? "Items" : "Item"]})'
    }),
    height: GRID_HEIGHT,
    id:'issues_grid',
	width: GRID_WIDTH,
	split: true,
	region: 'west'
});

grid_issues.on('dblclick', function(){ edit_issue() });

var markup_issues = [
	'<table class="project_table">',
	'<tr><th>Owner</th> <td>{owner}</td></tr>',
	'<tr><th>Description</th> <td>{description}</td></tr>',
	'<tr><th>Author</th> <td>{author}</td></tr>',
	'<tr><th>Type</th> <td>{type}</td></tr>',
	'<tr><th>Status</th> <td>{status}</td></tr>',
	'<tr><th>Priority</th> <td>{priority}</td></tr>',
	'<tr><th>Related RFC</th> <td>{related_rfc}</td></tr>',
	'<tr><th>Related Helpdesk</th> <td>{related_helpdesk}</td></tr>',
	'<tr><th>History</th> <td>{history_html}</td></tr>',
	'<tr><th>Created Date</th> <td>{created_date}</td></tr>',
	'<tr><th>Modified Date</th> <td>{modified_date}</td></tr>', '</table>' ];
var tpl_issues = new Ext.Template(markup_issues);

var panel_issues = new Ext.Panel({
	layout: 'border', height: 400,
	items: [ grid_issues, { id: 'issues_detail', bodyStyle: { background: '#ffffff', padding: '7px' }, region: 'center', html: 'Please select an Issue to see more details'} ]
});

grid_issues.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
		var panel_issues = Ext.getCmp('issues_detail');
		tpl_issues.overwrite(panel_issues.body, r.data);
});


/*
 *
 * Create the Lessons Learnt Grid
 *
 */

// Add Lesson
var lesson_fields = [
		{ xtype: "textarea", fieldLabel: "Description", name: "description", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "lesson-description"  },
		{ xtype: "checkbox", fieldLabel: "Publish to Client", name: "publish_to_client", ttEnabled: true, cmsSlug: "lesson-publish"  }
];

var add_lesson = function(b,e){
	var form_add_lesson = new Ext.form.FormPanel({ url: "/Lessons/" + project_number + "/Add/", bodyStyle: "padding: 15px;", autoScroll: true, items: lesson_fields });
	
	var window_lesson = new Ext.Window({width: 620, height:300, closeAction: "hide", autoScroll: true, modal: true, title: "Add a Lesson", items: [ form_add_lesson ],
				buttons: [ {	text: "Submit",
								handler: function(){
									form_add_lesson.getForm().submit({
										params: { author: user_id },
										success: function(f,a){
											Ext.message.msg("Success", "Lesson Added", 5);
											window_lesson.hide();
											Ext.getCmp("grid_lessons").store.load();
											Ext.getCmp("lessons_detail").body.update("Please select a lesson to see more details");
										},
										failure: function(f,a){
											Ext.Msg.alert("Warning", a.result.errormsg);	
										}
									});
								}},
							{ text: "Close", handler: function(){ window_lesson.hide(); }}]
	});
	project_menu.hide();
	tabpanel.activate(5);
	window_lesson.show();
	window_lesson.center();
};




/* Edit Lessons */
var edit_lessons = function(b,e){
	var	lessons_id = grid_lessons.getSelectionModel().getSelected().get("pk");
	var form_lessons_edit = new Ext.form.FormPanel({ url: "/Lessons/" + project_number + "/" + lessons_id + "/Edit/", bodyStyle: "padding: 15px;", autoScroll: true, items: lesson_fields});
	form_lessons_edit.getForm().load({ url: "/Lessons/" + project_number + "/" + lessons_id + "/", method: "GET" });
	var window_lessons = new Ext.Window({width: 620, height:540, closeAction: "hide", autoScroll: true, modal: true, title: "Edit Lesson", items: [ form_lessons_edit ],
							buttons: [ { text: 'Save',
                                         handler: function(){
                                         form_lessons_edit.getForm().submit({
											params: { author: user_id },
                                            success: function(f,a){
                                            			Ext.message.msg('Success', 'Lesson Updated', 5);
                                            					window_lessons.hide(); 
                                            					Ext.getCmp("grid_lessons").store.load();
                                            					Ext.getCmp("lessons_detail").body.update('Please select a lesson to see more details');
									    },  
                                            failure: function(f,a){
                                           Ext.Msg.alert('Warning', a.result.errormsg);
                                            }
                                        });
                                        }}   , { text: 'Close', handler: function(){ window_lessons.hide(); } }
									] 
	});
	window_lessons.show();
	window_lessons.center();
};


// Delete Lessons
function delete_lesson() {
	var lessonId = grid_lessons.getSelectionModel().getSelected().get("pk");
	var sm = grid_lessons.getSelectionModel();
	var sel = sm.getSelected();
	if (sm.hasSelection()){
		Ext.Msg.show({
			title: 'Remove Lesson',
			buttons: Ext.MessageBox.YESNO,
			msg: 'Remove <b>'+sel.data.description+'</b>?',
			closable: false, 
			fn: function(btn){
				if (btn == 'yes'){
						Ext.Ajax.request({
        url: "/Lessons/" + project_number + "/" + lessonId + "/Delete/",
        method: "POST",
        params: {"pk": lessonId
            
        },
        failure: function (response) {
            Ext.Msg.alert('Error', response.responseText);
        },
        success: function (response) {
            Ext.message.msg('Success', sel.data.description + " has been removed", 5);
           Ext.getCmp("grid_lessons").store.load();
           Ext.getCmp("lesson_detail").body.update('Please select a lesson to see more details');
           }
    });
				}
			}
		});
	}
};


var st_lessons = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: "/Lessons/" + project_number + "/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [
		{name:"pk", mapping: "pk"},
		{ name: "author", mapping: "fields.author.extras.get_full_name" },
		{ name: "description", mapping: "fields.description" },
		{ name: "created_date", mapping: "fields.created_date", type: "date", dateFormat: JSON_DATE },
		{ name: "modified_date", mapping: "fields.modified_date", type: "date", dateFormat: JSON_DATE },
		{ name: "publish_to_client", mapping: "fields.publish_to_client" } ]}),
	autoLoad: true
});

var btn_update_lesson = { iconCls: 'icon-update', text: 'Update Lesson', handler: edit_lessons };
var btn_delete_lesson = { iconCls: 'icon-complete', text: 'Delete Lesson', handler: delete_lesson };

var grid_lessons = new Ext.grid.GridPanel({
	store: st_lessons,
	columns: [
            {header: "Description", dataIndex: 'description'},
            {header: "Author", dataIndex: 'Author', hidden: true, sortable: true },
            {header: "Created Date", dataIndex: 'created_date', hidden: true, sortable: true, renderer: DATE_RENDERER },
            {header: "Modified Date", dataIndex: 'modified_date', hidden: true, sortable: true, renderer: DATE_RENDERER },
            {xtype: "booleancolumn", header: "Publish To Client", dataIndex: 'publish_to_client', sortable: true }
	],
    tbar: [ btn_update_lesson, btn_delete_lesson ],
	sm: new Ext.grid.RowSelectionModel({singleSelect: true}),
	viewConfig: { forceFit: true },
    height: GRID_HEIGHT,
    id:'grid_lessons',
	width: GRID_WIDTH,
	split: true,
	region: 'west'
});

grid_lessons.on('dblclick', function(){ edit_lesson() });

var markup_lessons = [
	'<table class="project_table">',
	'<tr><th>Description</th> <td>{description}</td></tr>',
	'<tr><th>Author</th> <td>{author}</td></tr>',
	'<tr><th>Publish To Client</th> <td>{publish_to_client}</td></tr>',
	'<tr><th>Created Date</th> <td>{created_date}</td></tr>',
	'<tr><th>Modified Date</th> <td>{modified_date}</td></tr>', '</table>' ];
var tpl_lessons = new Ext.Template(markup_lessons);

var panel_lessons = new Ext.Panel({
	layout: 'border', height: 400,
	items: [ grid_lessons, { id: 'lessons_detail', bodyStyle: { background: '#ffffff', padding: '7px' }, region: 'center', html: 'Please select an Lesson to see more details'} ]
});

grid_lessons.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
		var panel_lessons = Ext.getCmp('lessons_detail');
		tpl_lessons.overwrite(panel_lessons.body, r.data);
});



/*
 * Add/Edit/Delete Files
*/
var st_file_type = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[1,"Project Plan"],[2,"Other File"]]});


var file_fields = [
	{ xtype: "textarea", fieldLabel: "Description", name: "description", width: TEXTAREA_WIDTH, height: TEXTAREA_HEIGHT, ttEnabled: true, cmsSlug: "file-description"  },
	{ xtype: "combo", fieldLabel: "File Type", hiddenName: "file_type", displayField: "d", valueField: "id", store: st_file_type, mode: "local", triggerAction: "all", ttEnabled: true, cmsSlug: "file-type", editable: false  },
	{ xtype: "combo", fieldLabel: "Author", hiddenName: "author",  lazyInit: false,  store: st_users, mode: "local", displayField: "username", valueField: "pk", triggerAction: "all", ttEnabled: true, cmsSlug: "file-author", editable: false  },
	{ xtype: 'fileuploadfield', id: 'form-file', emptyText: 'Select an file', fieldLabel: 'File', name: 'filename',  buttonText: '', buttonCfg: { iconCls: 'upload-icon' }, ttEnabled: true, cmsSlug: "file-upload" }
];



var add_file = function(b,e){
	var form_add_file = new Ext.form.FormPanel({ url: "/Files/" + project_number + "/AddFile/", bodyStyle: "padding: 15px;", autoScroll: true, items: file_fields, fileUpload: true });
	var window_file = new Ext.Window({autoHeight: true, width: 650 , closeAction: "close", autoScroll: true, modal: true, title: "Add a File", items: [ form_add_file ],
				buttons: [ {	text: "Submit",
								handler: function(){
									form_add_file.getForm().submit({
										success: function(f,a){
											Ext.message.msg("Success", "File Added", 5);
											window_file.destroy();
											Ext.getCmp("grid_files").store.load();
											Ext.getCmp("file_detail").body.update("Please select a File to see more details");
										},
										failure: function(f,a){
											Ext.Msg.alert("Warning", a.result.errormsg);	
										}
									});
								}},
							{ text: "Close", handler: function(){ window_file.destroy(); }}]
	});
	tabpanel.activate(7);
	window_file.show();
	window_file.center();
};


function delete_file() {
	var fileId = grid_file.getSelectionModel().getSelected().get("pk");
	var sm = grid_file.getSelectionModel();
	var sel = sm.getSelected();
	if (sm.hasSelection()){
		Ext.Msg.show({
			title: 'Remove File',
			buttons: Ext.MessageBox.YESNO,
			msg: 'Remove <b>'+sel.data.description +'</b>?',
			closable: false, 
			fn: function(btn){
				if (btn == 'yes'){
						Ext.Ajax.request({ url: "/Files/" + project_number + "/Delete/", method: "POST", params: {"pk": sel.data.pk },
        					failure: function (response) { Ext.Msg.alert('Error', response.responseText); },
        					success: function (response) {
            					Ext.message.msg('Success', sel.data.description + " has been removed", 5);
           						Ext.getCmp("grid_files").store.load();
           						Ext.getCmp("file_detail").body.update('Please select a file to see more details');
           					}
    					});
				}
			}
		});
	};
}


var st_file = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: "/Files/" + project_number + "/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [
		{ name: "pk", mapping: "pk" },
		{ name: "description", mapping: "description" },
		{ name: "file_type", mapping: "file_type" },
		{ name:"created_date", type: "date", dateFormat: JSON_DATE, mapping: "created_date"},
		{ name: "author", mapping: "author" }
		]}),
	autoLoad: true
});

var btn_add_file = { iconCls: 'icon-add', text: 'Add File', handler: add_file }
var btn_delete_file = { iconCls: 'icon-complete', text: 'Delete File', handler: delete_file }

var renderer_file = function(val, x, data){
	return "<a href='" + data.json.url + "'>" + val + "</a>"

} 

var grid_file = new Ext.grid.GridPanel({
	store: st_file,
	columns: [
            {header: "Description", dataIndex: 'description', renderer: renderer_file },
            {header: "File Type", dataIndex: 'file_type', sortable: true},
            {header: "Author", dataIndex: 'author', sortable: true },
            {header: "Created Date", dataIndex: 'created_date', sortable: true, hidden: true, renderer: DATE_RENDERER }
	],
    tbar: [ btn_add_file, btn_delete_file ],
	sm: new Ext.grid.RowSelectionModel({singleSelect: true}),
	viewConfig: { forceFit: true },
	id:'grid_files',
    height: GRID_HEIGHT,
	width: GRID_WIDTH,
	split: true,
	region: 'west'
});

var markup_files = [
	'<table class="project_table">',
	'<tr><th>Description</th> <td>{description}</td></tr>',
	'<tr><th>File Type</th> <td>{file_type}</td></tr>',
	'<tr><th>Created Date</th> <td>{created_date}</td></tr>',
	'</table>' ]
var template_files = new Ext.Template(markup_files);

var panel_files = new Ext.Panel({
	layout: 'border', height: 400,
	items: [ grid_file, { id: 'file_detail', bodyStyle: { background: '#ffffff', padding: '7px' }, region: 'center', html: 'Please select an File to see more details'} ]
});

grid_file.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
		var detailPanel = Ext.getCmp('file_detail');
		template_files.overwrite(detailPanel.body, r.data);
});








/*
 *
 * Create the Project Report Grid
 *
 */
var st_report_type = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[1,"Checkpoint Report"],[2,"Executive Summary"]]});
 
 var report_fields = [
		{ xtype: "textarea", fieldLabel: "Summary", name: "summary", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "report-summary"  },
		{ xtype: "combo", fieldLabel: "Type", hiddenName: "type", name: "type", lazyInit: false, store: st_report_type, mode: "local", displayField: "d", valueField: "id", triggerAction: "all", ttEnabled: true, cmsSlug: "report-type", editable: false  } ]
 
  /* Edit Reports */
 var edit_report = function(b,e){
	var	report_id = grid_report.getSelectionModel().getSelected().get("pk");
	var form_report_edit = new Ext.form.FormPanel({ url: "/Projects/" + project_number + "/Reports/" + report_id + "/Edit/", bodyStyle: "padding: 15px;", autoScroll: true, items: report_fields});
	form_report_edit.getForm().load({ url: "/Projects/" + project_number + "/Reports/" + report_id + "/", method: "GET" });
	var window_report = new Ext.Window({width: 620, height:348, closeAction: "hide", autoScroll: true, modal: true, title: "Edit Report", items: [ form_report_edit ],
							buttons: [ { text: 'Save',
                                         handler: function(){
                                         form_report_edit.getForm().submit({
											params: { author: user_id },
                                            success: function(f,a){
                                            Ext.message.msg('Success', 'Report Updated', 5);
                                            	window_report.hide(); 
                                            	Ext.getCmp("grid_reports").store.load();
                                            	Ext.getCmp("report_detail").body.update('Please select a report to see more details');
									    },  
                                            failure: function(f,a){
                                            Ext.Msg.alert('Warning', 'An Error occured');
                                            }
                                        });
                                        }}   , { text: 'Close', handler: function(){ window_report.hide(); } }] });
	window_report.show();
	window_report.center();

}

var add_report = function(b,e){
	var form_add_report = new Ext.form.FormPanel({ url: "/Projects/" + project_number + "/Reports/Add/", bodyStyle: "padding: 15px;", autoScroll: true, items: report_fields });
	var window_report = new Ext.Window({width: 620, height:300,  closeAction: "hide", autoScroll: true, modal: true, title: "Add a Report", items: [ form_add_report ],
				buttons: [ {	text: "Submit",
								handler: function(){
									form_add_report.getForm().submit({
										params: { author: user_id },
										success: function(f,a){
											Ext.message.msg("Success", "Report Added", 5);
											window_report.hide();
											Ext.getCmp("grid_reports").store.load();
											Ext.getCmp("report_detail").body.update("Please select a Report to see more details");
										},
										failure: function(f,a){
											Ext.Msg.alert("Warning", a.result.errormsg);	
										}
									});
								}},
							{ text: "Close", handler: function(){ window_report.hide(); }}]
	});
	project_menu.hide();
	tabpanel.activate(6);
	window_report.show();
	window_report.center();
}

// Delete report
function delete_report() {
	var reportId = grid_report.getSelectionModel().getSelected().get("pk");
	var sm = grid_report.getSelectionModel();
	var sel = sm.getSelected();
	if (sm.hasSelection()){
		Ext.Msg.show({
			title: 'Remove Report',
			buttons: Ext.MessageBox.YESNO,
			msg: 'Remove <b>'+sel.data.summary +'</b>?',
			closable: false, 
			fn: function(btn){
				if (btn == 'yes'){
						Ext.Ajax.request({
        url: "/Projects/" + project_number + "/Reports/" + reportId + "/Delete/",
        method: "POST",
        params: {"pk": reportId
            
        },
        failure: function (response) {
            Ext.Msg.alert('Error', response.responseText);
        },
        success: function (response) {
            Ext.message.msg('Success', sel.data.summary + " has been removed", 5);
           Ext.getCmp("grid_reports").store.load();
           Ext.getCmp("report_detail").body.update('Please select a report to see more details');
           }
    });
				}
			}
		});
	};
}


var st_report = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: "/Projects/" + project_number + "/Reports/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [
		{ name: "pk", mapping: "pk" },
		{ name: "author", mapping: "fields.author.extras.get_full_name" },
		{ name: "type", mapping: "fields.type" },
		{ name: "created_date", mapping: "fields.created_date", type: "date", dateFormat: JSON_DATE },
		{ name: "modified_date", mapping: "fields.modified_date", type: "date", dateFormat: JSON_DATE },
		{ name: "summary", mapping: "fields.summary" } ]}),
	autoLoad: true
});

var btn_update_report = { iconCls: 'icon-update', text: 'Update Report', handler: edit_report }
var btn_delete_report = { iconCls: 'icon-complete', text: 'Delete Report', handler: delete_report }

var grid_report = new Ext.grid.GridPanel({
	store: st_report,
	columns: [
            {header: "Summary", dataIndex: 'summary'},
            {header: "Author", dataIndex: 'author', sortable: true},
            {header: "Created_date", dataIndex: 'created_date', hidden: true, sortable: true, renderer: DATE_RENDERER },
            {header: "Type", dataIndex: 'type', hidden: true, sortable: true },
            {header: "Modified Date", dataIndex: 'modified_date', sortable: true, hidden: true, renderer: DATE_RENDERER }
	],
    tbar: [ btn_update_report, btn_delete_report ],
	sm: new Ext.grid.RowSelectionModel({singleSelect: true}),
	viewConfig: { forceFit: true },
	id:'grid_reports',
    height: GRID_HEIGHT,
	width: GRID_WIDTH,
	split: true,
	region: 'west'
});

grid_report.on('dblclick', function(){ edit_report() });

var markup_report = [
	'<table class="project_table">',
	'<tr><th>Author</th><td>{author}</td></tr>',
	'<tr><th>Summary</th><td>{summary}</td></tr>',
	'<tr><th>Type</th><td>{type}</td></tr>',
	'<tr><th>Created Date</th><td>{created_date}</td></tr>',
	'<tr><th>Modified Date</th><td>{modified_date}</td></tr>', '</table>' ];
var tpl_report = new Ext.Template(markup_report);

var panel_report = new Ext.Panel({
	layout: 'border', height: 400,
	items: [ grid_report, { id: 'report_detail', bodyStyle: { background: '#ffffff', padding: '7px' }, region: 'center', html: 'Please select an Update to see more details'} ]
});

grid_report.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
		var panel_report = Ext.getCmp('report_detail');
		tpl_report.overwrite(panel_report.body, r.data);
});






/* 
 *
 * Edit the Project Initation data 
 *
 * */
var edit_project_initiation = function(b,e){
	var st_company = new Ext.data.Store({
		proxy: new Ext.data.HttpProxy({ url: "/xhr/get_companies/" }),
		reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk", mapping: "pk"},{name:"name", mapping: "fields.company_name"}]}),
		autoLoad: true
	});

	var st_project_status = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[0,"Proposed"],[1,"Draft"],[2,"Active"],[3,"On Hold"],[4,"Completed"],[5,"Archived"],[6,"Informational"]]});
	var st_duration_type = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[0,"Hours"],[1,"Days"]]});

	var project_initiation_fields = [
		{ xtype: "textfield", fieldLabel: "Project Name", name: "project_name", ttEnabled: true, cmsSlug: "project-name"  },
		{ xtype: "textfield", fieldLabel: "Project Number", name: "project_number", ttEnabled: true, cmsSlug: "project-number" },
		{ xtype: "combo", fieldLabel: "Project Status", hiddenName: "project_status", lazyInit: false,  store: st_project_status, mode: "local", displayField: "d", valueField: "id", triggerAction: "all", ttEnabled: true, cmsSlug: "project-status", editable: false },
		{ xtype: "combo", fieldLabel: "Company", hiddenName: "company", lazyInit: false,  store: st_company, mode: "local", displayField: "name", valueField: "pk", triggerAction: "all", ttEnabled: true, cmsSlug: "project-company", editable: false },
		{ xtype: "combo", fieldLabel: "Project Manager", hiddenName: "project_manager", lazyInit: false,  store: st_users, mode: "local", displayField: "username", valueField: "pk", triggerAction: "all", ttEnabled: true, cmsSlug: "project-manager", editable: false },

		{ xtype: 'itemselector', name: "team_managers_placeholder", hiddenName: 'team_managers_placeholder', fieldLabel: 'Team Managers',
	        imagePath: '/site_media/js/ext-3.2.0/examples/ux/images/',
			allowBlank: false,
            multiselects: [{
				legend: "Available People",
				scroll: true,
                width: 200,
                height: 200,
                store: st_non_managers,
                displayField: 'username',
                valueField: 'pk'
            },{
				legend: "Team Managers",
                width: 200,
                height: 200,
                store: st_managers,
                displayField: 'username',
                valueField: 'pk'
	        }], ttEnabled: true, cmsSlug: "project-team-managers"
		},

		{ xtype: "textfield", fieldLabel: "Project Sponsor", name: "project_sponsor", ttEnabled: true, cmsSlug: "project-sponsor" },
		{ xtype: "combo", fieldLabel: "Duration Time Unit", hiddenName: "duration_type", lazyInit: false,  store: st_duration_type, mode: "local", displayField: "d", valueField: "id", triggerAction: "all", ttEnabled: true, cmsSlug: "project-duration-type", editable: false },
		{ xtype: "textarea", fieldLabel: "Project Description", name: "project_description", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "project-description" },
		{ xtype: "textarea", fieldLabel: "Business Case", name: "business_case", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "project-business-case" },
		{ xtype: "textarea", fieldLabel: "Business Benefits", name: "business_benefits", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "project-business-benefits" },
		{ xtype: "textarea", fieldLabel: "Project Scope", name: "project_scope", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "project-scope" },
		{ xtype: "textarea", fieldLabel: "Exclusions", name: "exclusions", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "project-exclusions" },
		{ xtype: "textarea", fieldLabel: "Assumptions", name: "assumptions", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "project-assumptions" },
		{ xtype: "textarea", fieldLabel: "Communications Plan", name: "communications_plan", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "project-communications-plan" },
		{ xtype: "textarea", fieldLabel: "Quality Plan", name: "quality_plan", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, ttEnabled: true, cmsSlug: "project-quality-plan" }]
	var project_initiation_form = new Ext.form.FormPanel({url: "/Projects/" + project_number + "/Edit/EditPID/", bodyStyle: "padding: 15px;", autoScroll: true, items: project_initiation_fields });
	project_initiation_form.getForm().load({ url: "/xhr/" + project_number + "/edit_pid/", method: "GET" });
	var pid_win = new Ext.Window({width: 620, height:540, closeAction: "hide", autoScroll: true, modal: true, title: "Edit Project Initiation", items: [ project_initiation_form ],
							buttons: [ { text: 'Save',
                                         handler: function(){
                                         	// New Code Added
                                            		var itemCount = project_initiation_fields[5].multiselects[1].store.data.items.length;
                                            		var postString = new Array(itemCount);
                                            		
                                            		for(i = 0;i<itemCount;i++)
                                            		{
                                            			postString[i] = new Array(2);
                                            			postString[i][0] = "team_managers";
                                            			postString[i][1] = project_initiation_fields[5].multiselects[1].store.data.items[i].data.pk;
                                            		}
                                            		
//																								// End New Code Added
                                         	var jsondata = Ext.util.JSON.encode( postString );
                                         	
//                                        
                                         project_initiation_form.getForm().submit({
                                         	params: { paramsWithArrayJson: jsondata  },
                                            success: function(f,a){
                                            		
                                            Ext.message.msg('Success', 'Project Initiation Updated', 5);
						pid_win.hide(); 
						window.location.reload();
					    },  
                                            failure: function(f,a){
                                            Ext.Msg.alert('Warning', 'An Error occured');
                                            }
                                        });

					 
                                        }}   
									, { text: 'Close', handler: function(){ pid_win.hide(); } }] });
	project_menu.hide();
	tabpanel.activate(0);	
	pid_win.show();
	pid_win.center();
}


/*
 *
 * Build the Project Management menu 
 *
 * */
var project_menu =  new Ext.menu.Menu({	items: [{ text: "Add Deliverable", handler: add_deliverable}, 
											{ text: "Add Risk", handler: add_risk },
											{ text: "Add Issue", handler: add_issue },
											{ text: "Add Lesson Learnt", handler: add_lesson },
											{ text: "Add Report", handler: add_report },
											{ text: "Add File", handler: add_file },
											{ text: "Edit Project Initiation", handler: edit_project_initiation } ]});
var project_menu_button = { xtype: "tbbutton", text: "Manage Project", menu: project_menu }
toolbar.add(project_menu_button); 




// Project Timeline
var tl;

function onLoad() {
    var eventSource = new Timeline.DefaultEventSource();
    var bandInfos = [
        Timeline.createBandInfo({
            eventSource:    eventSource,
            width:          "70%", 
            intervalUnit:   Timeline.DateTime.WEEK, 
            intervalPixels: 100
        }),
        Timeline.createBandInfo({
            overview: true,
            eventSource:    eventSource,
            width:          "30%", 
            intervalUnit:   Timeline.DateTime.MONTH, 
            intervalPixels: 200
        })
    ];
    bandInfos[1].syncWith = 0;
    bandInfos[1].highlight = true;
                   
    tl = Timeline.create(document.getElementById("project_timeline"), bandInfos);
    Timeline.loadJSON("/WBS/" + project_number + "/Timeline/", function(json, url) { eventSource.loadJSON(json, url); });
    tl.layout();
}

var resizeTimerID = null;
function onResize() {
    if (resizeTimerID == null) {
        resizeTimerID = window.setTimeout(function() {
            resizeTimerID = null;
            tl.layout();
        }, 500);
    }
}

/* 
 *
 * Create tabs 
 *
 * */
tab_items = [
	{ xtype: "panel", contentEl: "project_initiation", title: "Project Initiation" },
	{ xtype: "panel", title: "Deliverables", items: [ panel_deliverables ], autoHeight: true },
	{ xtype: "panel", title: "Risks", items: [ risk_panel ], autoHeight: true  },
	{ xtype: "panel", title: "Work Items", items: [ panel_wbs ], autoHeight: true  },
	{ xtype: "panel", title: "Issues", items: [ panel_issues ], autoHeight: true  },
	{ xtype: "panel", title: "Lessons Learnt", items: [ panel_lessons ], autoHeight: true  },
	{ xtype: "panel", title: "Reports", items: [ panel_report ], autoHeight: true  },
	{ xtype: "panel", title: "Files", items: [ panel_files ], autoHeight: true  } ]

var tabpanel = new Ext.TabPanel({ items: tab_items, bodyStyle: "padding: 15px;", activeTab: 0, autoDestroy: false});	

// Function to add the Project Timeline to the tabpanel
var add_timeline_to_tabs = function(){
    Ext.Msg.alert('Message from Developer', 'The Project timeline feature is still experimental and has some small issues.<br>To activate the timeline please resize your browser');
    tabpanel.add({ title: "Time Line", contentEl: 'project_timeline_wrapper', closable: true, autoHeight: true }).show();
};

// Function to open the Gantt chart in a new browser window
var open_gantt = function(){
    window.open("/WBS/" + project_number + "/JsGantt/", "gantt_window");
};

var project_view_menu = new Ext.menu.Menu({ items: [
    { text: "View Project Timeline", handler: add_timeline_to_tabs },
    { text: "View Gantt", handler: open_gantt }
    ]});
var project_view_menu_button = { xtype: "tbbutton", text: "View", menu: project_view_menu };
toolbar.add(project_view_menu_button);


center_panel.items = [ toolbar, tabpanel ]
