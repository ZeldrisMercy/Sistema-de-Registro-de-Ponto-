Sistema de Ponto

📌 Sobre o Projeto
Este software foi desenvolvido para automatizar o gerenciamento e cálculo de horas trabalhadas para uma empresa privada. O sistema elimina a necessidade de cálculos manuais complexos, reduzindo erros humanos e garantindo a integridade dos dados de ponto, bem como automatiza um cálculo que antes poderia levar horas.

🛠️ Tecnologias Utilizadas
Linguagem: Python 3.12.

Interface: Tkinter (ou a biblioteca que você usou para a UI).

Distribuição: PyInstaller (para empacotamento).

Instalador: Inno Setup Compiler (para geração do executável profissional).

🚀 Funcionalidades
Registro de entrada, saída e intervalos.

Cálculo Automático: Conversão de horas e minutos (base 60) para evitar erros de soma sexagesimal.

Instalador Customizado: Interface de instalação com a identidade visual da empresa e gestão automática de dependências (_internal).

📂 Estrutura de Distribuição
O projeto utiliza o modo --onedir do PyInstaller para melhor performance. A estrutura de arquivos instalada segue o padrão:

Ponto AMAN.exe: Executável principal.

_internal/: Pasta contendo bibliotecas dinâmicas (DLLs), incluindo python312.dll, garantindo que o software rode em máquinas sem Python instalado.

⚙️ Como Instalar
Vá até a pasta APP/ deste repositório.

Execute o arquivo mysetup.exe.

Siga as instruções do assistente (requer privilégios de administrador para instalação em Program Files).

👤 Autor
Ícaro de Souza Mariano (ZeldrisMercy)

Estudante de Sistemas de Informação.

Aspirante a Cyber Defender & Cisco CyberOps Associate.
