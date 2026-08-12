# MoCapLibras 🤟

**Desenvolvimento de um Pipeline em Unreal Engine para Captura de Movimentos e Animação de Alta Fidelidade em Libras.**

Este repositório contém os arquivos de projeto, códigos-fonte e materiais suplementares referentes ao artigo **"MoCapLibras"**, submetido ao *XXV Workshop de Ferramentas e Aplicações (WFA)* do WebMedia. 

O objetivo principal deste projeto é democratizar a geração de avatares tridimensionais (MetaHumans) que traduzam a Língua Brasileira de Sinais (Libras) com alta fidelidade, mitigando o efeito "Vale da Estranheza" ao capturar Sinais Não-Manuais (expressões faciais e postura corporal) usando câmeras de vídeo convencionais (*Markerless Motion Capture*).

---

## 📁 Estrutura do Repositório

* **`/Video dos Sinalizadores`**: Contém os vídeos originais (em formato `.mp4`) recortados em 30 segundos, provenientes do Corpus de Libras, bem como as animações finais exportadas e os *Rigs* resultantes do processamento.
* **`/Ensaios_AoVivo`**: Contém os scripts em Python desenvolvidos com a biblioteca **MediaPipe**. Este módulo experimental serve para a captura de movimentos espaciais em tempo real, enviando os dados diretamente para a Unreal Engine via protocolo Live Link.
* **Outras Pastas (`/Content`, `/Config`, etc.)**: Alguns dos arquivos brutos do projeto da Unreal Engine.

---

## ⚙️ Requisitos do Sistema

* **Motor Gráfico:** Unreal Engine 5.8.1 (com pacote *MetaHuman Creator* baixado).
* **Hardware Recomendado:** Windows 11, CPU Quad-core 2.5 GHz, 32 GB RAM, GPU NVIDIA RTX Série 2000 ou superior (O projeto foi testado em uma RTX 4060 8GB).
* **Para uso ao vivo (Python):** Python 3.8+ e bibliotecas listadas no `requirements.txt` da respectiva pasta.

---

## 🚀 Como Utilizar o Projeto Pronto

Se você deseja abrir o projeto com todas as configurações, luzes e *MetaHumans* já montados, siga os passos abaixo para importar os arquivos deste repositório:

1. Abra a Unreal Engine 5.8.1.
2. Crie um **Novo Projeto** em branco (`Blank`) na categoria **Film, Video & Live Events**.
3. Feche a Unreal Engine.
4. Faça o download ou clone este repositório (`git clone https://github.com/SEU_USUARIO/MoCapLibras.git`).
5. Copie as pastas principais (como `Content` e `Config`) que estão na raiz deste repositório e **cole dentro da pasta do projeto que você acabou de criar** no seu computador, substituindo os arquivos quando solicitado.
6. Abra o seu projeto novamente na Unreal. Os avatares e as animações já estarão disponíveis no *Content Browser*!

---

## 🎬 Reproduzindo o Pipeline (Tutorial)

Caso queira processar o seu próprio vídeo e aplicar no MetaHuman do zero (conforme demonstrado no vídeo tutorial do artigo), siga o fluxo abaixo:

### 1. Preparação e Ingestão
* Habilite os plugins: *MetaHuman Animator*, *Markerless Motion Capture*, *Live Link* e *Live Link Hub*.
* Abra o **Live Link Hub** e adicione o módulo `Mono Video Ingest`.
* Selecione o seu vídeo `.mp4` (recomendado: 1080p a 30fps) e aguarde a extração dos quadros.

### 2. Rastreamento (Machine Learning)
* Crie um ativo **MetaHuman Performance**.
* Vincule os dados capturados (*Footage Capture Data*) ao *Blueprint* do seu personagem.
* Processe o **Rastreamento Facial** (desmarcando o movimento da cabeça) e, em seguida, o **Rastreamento Corporal** (este processo é custoso e pode levar alguns minutos dependendo da sua GPU).

### 3. Sincronização (Bake to Control Rig)
* Crie uma nova **Level Sequence** e arraste o seu MetaHuman para a linha do tempo.
* Remova o *Control Rig* padrão para evitar sobreposições geométricas.
* Adicione a animação processada, clique com o botão direito e escolha **Bake to Control Rig** utilizando o perfil `MetaHuman_ControlRig`.
* Renderize a cena final utilizando um *Cine Camera Actor*.

---

## 🐍 Uso ao Vivo (MediaPipe)

A pasta `/Ensaios_AoVivo` contém uma prova de conceito para pular a etapa de processamento de vídeo gravado e usar a webcam em tempo real.

1. Navegue até a pasta: `cd Ensaios_AoVivo`
2. Instale as dependências: `pip install -r requirements.txt` (inclui `mediapipe`, `opencv-python`, etc).
3. Execute o script principal: `python live_mocap.py`
4. Na Unreal Engine, certifique-se de que o **Live Link** está escutando a porta UDP configurada no script Python para receber as rotações ósseas ao vivo.

---

## 📄 Licença

Este projeto é disponibilizado sob a licença **MIT**. A documentação, os scripts e os fluxos de trabalho podem ser utilizados, modificados e distribuídos livremente pela comunidade. 

*(Os vídeos do Corpus de Libras possuem direitos e licenças próprias de seus respectivos autores).*

---

**Autores:** [Nomes Omitidos para Revisão por Pares Duplo-Cega]  
**Contato:** [E-mail Omitido]
