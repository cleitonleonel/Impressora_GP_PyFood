# Impressora_GP_PyFood

Servidor Flask para comunicação com impressoras locais a partir do [Gestor de Pedidos](https://gestordepedidos.ifood.com.br/#/login)

<img src="https://raw.githubusercontent.com/cleitonleonel/Impressora_GP_PyFood/master/static/media/icons/png/AppIcon.png" alt="Impressora_GP_PyFood" width="250"/>

## OBS:
Esta é uma implementação em python baseada na versão node desse projeto que pode ser encontrada aqui [Impressora_GP_iFood](https://github.com/cleitonleonel/Impressora_GP_iFood)
O objetivo desse projeto se deu pelo fato de que o gestor de pedidos disponibilizado para download não cobre sistemas linux
bem como o app de impressão oficial, diante disso resolvi implementar algo de forma prática e funcional e é o que temos aqui.

## Clonando o projeto:

```shell
git clone https://github.com/cleitonleonel/Impressora_GP_PyFood.git
```

## Instalando CUPS:

É sempre uma boa prática atualizar os repositórios antes de instalar novos pacotes.

1. **Atualize o sistema**:
   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. **Instale o CUPS**:
   Execute o seguinte comando para instalar o CUPS.

   ```bash
   sudo apt install cups build-essential cmake libcups2-dev libcupsimage2-dev system-config-printer -y
   ```

3. **Inicie o serviço do CUPS**:
   Após a instalação, inicie o serviço CUPS.

   ```bash
   sudo systemctl start cups
   ```

4. **Ative o CUPS para iniciar no boot**:
   Para garantir que o CUPS inicie automaticamente em cada inicialização do sistema, use o seguinte comando:

   ```bash
   sudo systemctl enable cups
   ```

5. **Acesse a interface da web do CUPS**:
   Abra um navegador e acesse a interface web do CUPS para adicionar e gerenciar impressoras. Digite o seguinte URL:

   ```
   http://localhost:631

## Uso:
```shell
cd Impressora_GP_PyFood
pip install -r requirements.txt
python server.py
```

# Este projeto ajudou você?

Se esse projeto deixar você ficar à vontade para fazer uma doação =), pode ser R $ 0,50 hahahaha. Para isso, basta ler o qrcode abaixo, ele foi gerado com meu outro projeto chamado [Pypix](https://github.com/cleitonleonel/pypix.git) arquivo de amostra.

<img src="https://github.com/cleitonleonel/pypix/blob/master/qrcode.png?raw=true" alt="Your image title" width="250"/>

# Desenvolvido por:

Cleiton Leonel Creton ==> cleiton.leonel@gmail.com
