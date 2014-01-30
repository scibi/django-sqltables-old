/*
 * Part of django-tables
 *
 */

function SQLTable(table_id, app_name, table_name, options) {
	console.log('SQLTable - constructor');

	var t=this;

	this.table_id = table_id;
	this.app_name = app_name;
	this.table_name = table_name;
	this.base_url = '/tables/'+app_name+'/'+table_name;
	this.options = options || {};
    this.ready = false;

	init_table();


	function init_table() {
		console.log('SQLTable - constructor - init_table');
		$.getJSON( t.base_url+'/definition', function( data ) {
            var tmp="<table id=\""+t.table_id+"_table\"></table>";
            tmp+="<div id=\""+t.table_id+"_pager\"></div>";
			$('#'+t.table_id).html(tmp);
            
            console.log(data);
            var col_names=[];
            var col_models=[]
			$.each( data['columns'], function( key, val ) {
				col_names.push(val['label']);
                col_models.push({name:val['name'],index:val['name']});
            });
            console.log(col_models);
            var jqg_config={
                url: t.base_url+'/data',
                datatype: "json",
                height: 200,
                rowNum: 10,
                rowList: [10,20,30],
                colNames: col_names,
                colModel: col_models,
                pager: "#"+t.table_id+"_pager",
                viewrecords: true,
                /*caption: "Data",*/
                sortname: data['default_sort_by'],
                hidegrid:false
            };
            if (data['caption']) {
                jqg_config['caption']=data['caption'];
            }
			if (data['params']) {
                console.log(data['params']);
                jqg_config['postData'] = {}
                $.each( data['params'], function( key, val ) {
                    console.log(val);
                    jqg_config['postData']["param_"+val]=t.options['param_functions'][val];
                });
			}
            console.log(jqg_config);
            t.grid=jQuery("#"+t.table_id+"_table").jqGrid(jqg_config);

            // Setup buttons
            jQuery("#"+t.table_id+"_table")
            .jqGrid('navGrid',"#"+t.table_id+"_pager",
                {edit:false, add:false, del:false, search:false},
                {height:200,reloadAfterSubmit:true}
            );

            if (data['enable_download']) {
                jQuery("#"+t.table_id+"_table")
                .jqGrid('navButtonAdd',"#"+t.table_id+"_pager",{
                    title:"Download", 
                    caption: "",
                    buttonicon:"ui-icon-disk",
                    onClickButton: function(){ 
                        alert("Pobierz");
                    }, 
                    position:"last"
                });
            }


            // Setup filters
            jQuery("#"+t.table_id+"_table").jqGrid('filterToolbar',{defaultSearch:true,stringResult:true});

            // Set grid width to #content
            $("#"+t.table_id+"_table").jqGrid('setGridWidth', $("#"+t.table_id).width(), true); 

            // Bootstrap customization
            $(".ui-pg-input").attr('class', 'form-control');

            t.ready=true;
/*
			var items = [];
            var f_items = []
            var f_config = []
			$.each( data['columns'], function( key, val ) {
				items.push( "<th>" + val['label'] + "</th>" );
                if (data['filtering_enabled']) {
                    f_items.push( "<th></th>" );
                    if('filter' in val) {
                        f_config.push(val['filter']);
                    } else {
                        f_config.push(null);
                    }
                }
				});
            var tmp='<thead>';
            if (data['filtering_enabled']) {
                tmp+='<tr class="filter">'+f_items.join( '' )+'</tr>';
            }
            tmp+='<tr>'+items.join( '' )+'</tr>';
            tmp+='</thead>';

			$('#'+t.table_id).html(tmp);

			
			var dt_config={
				"sAjaxSource": t.base_url+'/data',
                "bPaginate": data['paging'],
                "bProcessing": true,
                "bServerSide": true,
                "sDom": "<'row'<'col-xs-6'l><'col-xs-6'T>r>t<'row'<'col-xs-6'i><'col-xs-6'p>>",
                "oLanguage": {  // FIXME FIXME FIXME FIXME FIXME
                    "sLengthMenu": "Wyświetl _MENU_ pozycji na stronie",
                    "sZeroRecords": "Nie znaleziono pasujących pozycji",
                    "sInfo": "Pokazane pozycje od _START_ do _END_ spośród _TOTAL_",
                    "sInfoEmpty": "Brak pozycji",
                    "sInfoFiltered": "(wyfiltrowanych spośród _MAX_ wszystkich pozycji)"
                },
                "aLengthMenu": [[10, 25, 50, 100, 500, -1], [10, 25, 50, 100, 500, "wszystkie"]], // FIXME FIXME FIXME FIXME FIXME
                "oTableTools": {
                    "sSwfPath": "/static/tabletools/swf/copy_csv_xls_pdf.swf",
                    "aButtons": [ {
                        "sExtends": "print",
                        "sButtonText": "Drukuj",
                        "bShowAll": true
                    }, {
                        "sExtends": "download",
                        "sButtonText": "Pobierz CSV",
                        "sUrl": t.base_url+'/csv'
                    } ]
                }
			}
			if (data['params']) {
				dt_config["fnServerParams"] = function ( aoData ) {
					$.each( data['params'], function( key, val ) {
						aoData.push({ "name": "param_"+val, "value": t.options['param_functions'][val]});
					});

				}
			}
			t.table=$('#'+t.table_id).dataTable(dt_config);
            if (data['filtering_enabled']) {
                t.table.columnFilter({
                    'sPlaceHolder': 'head:after',
                    'aoColumns': f_config
                });
            }
            $('#'+t.table_id+' input').addClass('form-control input-sm');
            $('#'+t.table_id+' select').addClass('form-control input-sm');
            $('#'+t.table_id+'_length select').addClass('form-control input-sm');
            $('#'+t.table_id+'_wrapper div.DTTT_container a').removeClass();
            $('#'+t.table_id+'_wrapper div.DTTT_container a').addClass('btn btn-default');
            t.ready=true;*/
		});
	}
}


SQLTable.prototype.refresh = function() {
    console.log('SQLTable - refresh');
    console.log(this.grid);
    if (this.ready) {
        this.grid.trigger("reloadGrid");
    } else {
        console.log("SQLTable.refresh(): not ready");
    }
}
