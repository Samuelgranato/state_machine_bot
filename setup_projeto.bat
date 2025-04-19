@echo off
set "ROOT=auto_player"

:: Criação de diretórios
mkdir %ROOT%
cd %ROOT%

mkdir capture
mkdir detection
mkdir navigation
mkdir assets
mkdir assets\mobs
mkdir assets\minimaps
mkdir utils

:: Criação de arquivos principais
echo # Arquivo principal >> main.py
echo # Dependências >> requirements.txt
echo # Configurações do projeto >> config.py

:: capture/screen.py
echo # captura de tela com mss > capture\screen.py

:: detection/motion.py
echo # detecção de movimentos > detection\motion.py

:: detection/mob_recognition.py
echo # reconhecimento de mobs > detection\mob_recognition.py

:: navigation/minimap_reader.py
echo # leitura do minimapa > navigation\minimap_reader.py

:: navigation/path_planner.py
echo # planejamento de caminho > navigation\path_planner.py

:: utils/image_tools.py
echo # funções auxiliares para imagem > utils\image_tools.py

echo Estrutura criada com sucesso.
pause
