{application,config,
             [{description,"INI file configuration system for Apache CouchDB"},
              {vsn,"a83b75e"},
              {registered,[config,config_event]},
              {applications,[kernel,stdlib]},
              {mod,{config_app,[]}},
              {modules,[config,config_app,config_listener,config_listener_mon,
                        config_notifier,config_sup,config_util,
                        config_writer]}]}.
