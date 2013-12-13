

// Deliverables
var add_deliverable = function(b,e){
    window_add_deliverable = new WindowAddDeliverableUi();
    form_add_deliverable = Ext.getCmp('form_add_deliverable');
    form_add_deliverable.getForm().url = '/api/deliverables/' + project_number + '/?format=ext-json';
    window_add_deliverable.addButton({   text: 'Submit',
                                         handler: function(){
                                             Ext.getCmp('form_add_deliverable').getForm().submit({
                                                success: function(f,a){
                                                    Ext.message.msg('Success', 'Deliverable Added', 5);
                                                    window_add_deliverable.destroy();
                                                    Ext.getCmp('grid_deliverables').store.load();
                                                    Ext.getCmp('panel_deliverables_detail').body.update('Please select a deliverable to see more details');
                                                },
                                                failure: function(f,a){
                                                    Ext.msg('Failure!');
                                                }});
                                         }});

    window_add_deliverable.addButton({  text: 'Cancel',
                                        handler: function(){
                                            window_add_deliverable.destroy();
                                        }});
    window_add_deliverable.show();
}

var getRating = function(){
    Ext.getCmp("rating").setValue(((Ext.getCmp("probability").value * Ext.getCmp("impact").value) / 2));
}

//Risks
var add_risk = function(b,e){
    window_add_risk = new WindowAddRiskUi();
    form_add_risk = Ext.getCmp('form_add_risk');
    form_add_risk.getForm().url = '/api/risks/' + project_number + '/?format=ext-json';
    Ext.getCmp('probability').slider.addListener('change', getRating);
    Ext.getCmp('probability').slider.addListener('setValue', function(slider) { slider.getValue(); });
    Ext.getCmp('impact').slider.addListener('change', getRating);
    window_add_risk.addButton({ text: 'Submit',
                                handler: function(){
                                    Ext.getCmp('form_add_risk').getForm().submit({
                                        success: function(f,a){
                                            Ext.message.msg('Success', 'Risk Added', 5);
                                            window_add_risk.destroy();
                                            Ext.getCmp('grid_risks').store.load();
                                            Ext.getCmp('panel_risk_detail').body.update('Please select a risk to see more details');
                                        },
                                        failure: function(f,a){
                                            Ext.msg('Failure!');
                                        }});
                                    }});

    window_add_risk.addButton({ text: 'Cancel',
                                handler: function(){
                                    window_add_risk.destroy();
                                }});
    window_add_risk.show();
};


// WBS
var add_work_item = function(b,e){
    window_add_wbs = new WindowAddWBSUi();
    form_add_wbs = Ext.getCmp('form_add_wbs');
    form_add_wbs.getForm().url = '/api/wbs/' + project_number + '/?format=ext-json';
    window_add_wbs.addButton({ text: 'Submit',
                                handler: function(){
                                    Ext.getCmp('form_add_wbs').getForm().submit({
                                        success: function(f,a){
                                            Ext.message.msg('Success', 'Work Item Added', 5);
                                            window_add_wbs.destroy();
                                            Ext.getCmp('grid_wbs').store.load();
                                            Ext.getCmp('panel_wbs_detail').body.update('Please select a work item to see more details');
                                        },
                                        failure: function(f,a){
                                            Ext.msg('Failure!');
                                        }});
                                    }});

    window_add_wbs.addButton({ text: 'Cancel',
                                handler: function(){
                                    window_add_wbs.destroy();
                                }});
    window_add_wbs.show();
};




Ext.onReady(function(){
    var viewport = new TheViewportUi();
    var panel = new MyPanelUi();
    main_panel = Ext.getCmp('center_panel');
    main_panel.add(panel);


    // Deliverables

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
    Ext.getCmp('grid_deliverables').getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
        var detail_panel = Ext.getCmp('panel_deliverables_detail');
        template_deliverables.overwrite(detail_panel.body, r.data);
    });

    // Risks
    var markup_risks = [
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
    var template_risks = new Ext.Template(markup_risks)
    Ext.getCmp('grid_risks').getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
        var r_detail_panel = Ext.getCmp('panel_risks_detail');
        template_risks.overwrite(r_detail_panel.body, r.data);
    });



    // Assign the correct URLs to the stores and load them.. Ignore the
    // temporary var names
    var st1 = Ext.StoreMgr.lookup('st_deliverables');
    st1.proxy = new Ext.data.HttpProxy({url:'/api/deliverables/' + project_number + '/?format=ext-json'});
    st1.load()

    var st2 = Ext.StoreMgr.lookup('st_risks');
    st2.proxy = new Ext.data.HttpProxy({url:'/api/risks/' + project_number + '/?format=ext-json'});
    st2.load()

    var st3 = Ext.StoreMgr.lookup('st_resources');
    st3.proxy = new Ext.data.HttpProxy({url:'/api/projects/' + project_number + '/resources/?format=ext-json'});
    st3.load()

    var st5 = Ext.StoreMgr.lookup('st_wbs');
    st5.proxy = new Ext.data.HttpProxy({url:'/api/wbs/' + project_number + '/?format=ext-json'});
    st5.load()

    var st6 = Ext.StoreMgr.lookup('st_stage_plan');
    st6.proxy = new Ext.data.HttpProxy({url:'/api/stageplan/' + project_number + '/?format=ext-json'});
    st6.load()

    Ext.getCmp('btn_add_deliverable').handler = add_deliverable;
    Ext.getCmp('menu_add_deliverable').addListener('click', add_deliverable);
    Ext.getCmp('btn_add_risk').handler = add_risk;
    Ext.getCmp('menu_add_risk').addListener('click', add_risk);
    Ext.getCmp('btn_add_wbs').handler = add_work_item;
    Ext.getCmp('menu_add_wbs').addListener('click', add_work_item);
    main_panel.doLayout();	

});
	    
