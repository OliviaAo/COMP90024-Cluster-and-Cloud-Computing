{application,couch_index,
             [{description,"CouchDB Secondary Index Manager"},
              {vsn,"53555fd"},
              {modules,[couch_index,couch_index_app,couch_index_compactor,
                        couch_index_epi,couch_index_plugin,couch_index_server,
                        couch_index_sup,couch_index_updater,couch_index_util]},
              {registered,[couch_index_server]},
              {applications,[kernel,stdlib,couch_epi]},
              {mod,{couch_index_app,[]}}]}.
