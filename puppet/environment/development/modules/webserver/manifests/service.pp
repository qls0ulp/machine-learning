### Note: the prefix 'webserver::', corresponds to a puppet convention:
###
###       https://github.com/jeff1evesque/machine-learning/issues/2349
###
class webserver::service {
    ## variables
    $webroot       = '/vagrant'
    $log_path      = "${webroot}/log/webserver/flask.log"
    $template_path = 'webserver/webserver.erb'

    ## include webserver dependencies
    include python
    include python::flask
    include python::requests

    ## dos2unix: convert clrf (windows to linux) in case host machine is
    #            windows.
    file { '/etc/init/flask.conf':
        ensure  => file,
        content => dos2unix(template($template_path)),
    }
}