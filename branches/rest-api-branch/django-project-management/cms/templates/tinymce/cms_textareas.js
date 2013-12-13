var use_tinymce = true;
tinyMCE.init({
    mode: "exact",
    theme: "advanced",
    plugins: "advimage,advlink,table,searchreplace,contextmenu,template,paste,save,spellchecker,autosave",
    // Appearance
    width: 480,
    height: 300,
    theme_advanced_buttons1: "save,template,separator,pastetext,separator,bold,italic,separator,bullist,numlist,separator,link,unlink,anchor,separator,image,separator,code",
    theme_advanced_buttons2: "spellchecker,search,replace,cleanup,separator,formatselect,separator,help",
    theme_advanced_buttons3: "",
    theme_advanced_blockformats: "p,h2,h3",
    // Styles
//    content_css: "media/css/tinymce_style.css",
    show_styles_menu: false,
    // (X)HTML
    forced_root_blok: 'p',
    extended_valid_elements: 'a[class|name|href|title|onclick],img[class|src|alt=image|title|onmouseover|onmouseout],p[id|style|dir|class],span[class|style]',
    invalid_elements: "font,strike,u",
    file_browser_callback: "CustomFileBrowser",
    external_link_list_url: "/cms/tiny_mce_links.js",
    gecko_spellcheck: true,
    language: "{{ language }}",
    directionality: "{{ directionality }}",
    spellchecker_languages : "{{ spellchecker_languages }}",
    spellchecker_rpc_url : "{{ spellchecker_rpc_url }}"
});

function CustomFileBrowser(field_name, url, type, win) {

    var cmsURL = "/admin/filebrowser/?pop=2";
    cmsURL = cmsURL + "&type=" + type;
    
    tinyMCE.activeEditor.windowManager.open({
        file: cmsURL,
        width: 820,  // Your dimensions may differ - toy around with them!
        height: 500,
        resizable: "yes",
        scrollbars: "yes",
        inline: "no",  // This parameter only has an effect if you use the inlinepopups plugin!
        close_previous: "no",
    }, {
        window: win,
        input: field_name,
        editor_id: tinyMCE.selectedInstance.editorId,
    });
    return false;
}
