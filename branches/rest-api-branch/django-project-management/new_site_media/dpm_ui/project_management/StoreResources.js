/*
 * File: StoreResources.js
 * Date: Thu Oct 21 2010 17:31:20 GMT+0100 (BST)
 * 
 * This file was generated by Ext Designer version xds-1.0.2.14.
 * http://www.extjs.com/products/designer/
 *
 * This file will be auto-generated each and everytime you export.
 *
 * Do NOT hand edit this file.
 */

StoreResources = Ext.extend(Ext.data.JsonStore, {
    constructor: function(cfg) {
        cfg = cfg || {};
        StoreResources.superclass.constructor.call(this, Ext.apply({
            storeId: 'st_resources',
            root: 'data',
            fields: [
                {
                    name: 'id',
                    mapping: 'id'
                },
                {
                    name: 'data',
                    mapping: 'username'
                }
            ]
        }, cfg));
    }
});
new StoreResources();