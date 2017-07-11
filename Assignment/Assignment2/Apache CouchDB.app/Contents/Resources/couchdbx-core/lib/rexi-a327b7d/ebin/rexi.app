{application,rexi,
             [{description,"Lightweight RPC server"},
              {vsn,"a327b7d"},
              {modules,[rexi,rexi_app,rexi_buffer,rexi_monitor,rexi_server,
                        rexi_server_mon,rexi_server_sup,rexi_sup,rexi_utils]},
              {registered,[rexi_sup,rexi_server]},
              {applications,[kernel,stdlib,couch_log,couch_stats,config]},
              {mod,{rexi_app,[]}}]}.
