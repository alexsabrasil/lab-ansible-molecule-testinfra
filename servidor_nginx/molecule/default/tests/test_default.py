def test_nginx_instalado_e_rodando(host):
    # Verifica se o pacote Nginx está instalado
    pacote_nginx = host.package("nginx")
    assert pacote_nginx.is_installed

    # Verifica se o serviço está ativo e habilitado
    servico_nginx = host.service("nginx")
    assert servico_nginx.is_running
    assert servico_nginx.is_enabled

    # Verifica se a porta 80 está escutando conexões
    porta_web = host.socket("tcp://0.0.0.0:80")
    assert porta_web.is_listening
