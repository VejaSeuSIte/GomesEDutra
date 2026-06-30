# -*- coding: utf-8 -*-
import json, html
from pathlib import Path
S = Path('C:/Users/gabri/GomesEDutra/scripts')
OUT = Path('C:/Users/gabri/GomesEDutra/assets/landings-content.json')


def load(name):
    raw = (S / name).read_text(encoding='utf-8')
    return json.loads(html.unescape(raw))

data = {}
for f in ['_prev.json', '_crim.json', '_civ.json']:
    data.update(load(f))

WA = 'https://wa.me/5500000000000'

data['sobre'] = {
    "slug": "sobre", "nav": "sobre", "related_category": None,
    "page_title": "Sobre · João Rocha Advocacia · OAB/UF 000.000",
    "page_description": "Conheça João Rocha, advogado atuante em Direito Criminal, Cível e Previdenciário. Atuação estratégica, sigilosa e humanizada, com atendimento online em todo o Brasil.",
    "eyebrow": "Quem Somos",
    "h1": "<em>João Rocha</em>, advogado.",
    "subtitle": "Advocacia e consultoria jurídica em Direito Criminal, Cível e Previdenciário — atuação técnica, sigilosa e próxima do cliente, com atendimento online em todo o Brasil.",
    "cta_text": "Falar com o escritório no WhatsApp",
    "wa_text": "Olá, João Rocha. Vim pela página Sobre.",
    "intro": {
        "h2": "Advocacia <em>estratégica</em> e ao lado de quem precisa.",
        "paragraphs": [
            "\"<em>Cada caso é uma história e uma pessoa por trás dele. Meu compromisso é ouvir com atenção, estudar com profundidade e conduzir cada demanda com técnica, ética e transparência — para que você entenda cada passo e decida com segurança.</em>\"",
            "O escritório <strong>João Rocha Advocacia e Consultoria Jurídica</strong> atua em três grandes frentes: <strong>Direito Criminal</strong> (defesa em inquéritos, prisões, audiências, habeas corpus e Tribunal do Júri, com firmeza e sigilo), <strong>Direito Previdenciário</strong> (aposentadorias, pensões, BPC/LOAS e revisões junto ao INSS, com justiça e acolhimento) e <strong>Direito Cível</strong> (indenizações, contratos, cobranças e família, com foco em resultados).",
            "Nosso método é <strong>objetivo e humano</strong>: ler o caso por inteiro, devolver ao cliente um diagnóstico honesto e agir com estratégia. Atendimento ágil pelo WhatsApp, sigilo profissional e total transparência nos honorários, combinados por escrito antes de qualquer trabalho. Atendemos presencialmente, com hora marcada, e <strong>online em todo o Brasil</strong>."
        ]
    },
    "bullets_eye": "Princípios do escritório",
    "bullets_h2": "O que <em>orienta</em> nosso trabalho.",
    "bullets": [
        {"title": "Atuação estratégica", "text": "Estudamos cada caso a fundo e definimos a melhor estratégia antes de agir — no criminal, no previdenciário e no cível."},
        {"title": "Sigilo e seriedade", "text": "Atendimento confidencial e conduta ética em cada etapa, com respeito ao Estatuto da Advocacia e ao seu momento."},
        {"title": "Atendimento ágil", "text": "Respostas rápidas pelo WhatsApp e acompanhamento próximo: você nunca fica sem saber o andamento do seu caso."},
        {"title": "Transparência total", "text": "Honorários combinados por escrito antes de iniciar, sem cobranças surpresa, com um diagnóstico honesto desde o primeiro contato."}
    ],
    "faq": [
        {"q": "Em quais áreas o escritório atua?", "a": "Em três frentes principais: <strong>Direito Criminal</strong>, <strong>Direito Previdenciário</strong> (INSS) e <strong>Direito Cível</strong> (incluindo família, contratos, cobranças e indenizações). Avaliamos o seu caso e indicamos o melhor caminho."},
        {"q": "Onde vocês atendem?", "a": "Atendemos presencialmente, com hora marcada, e <strong>online em todo o Brasil</strong> — por WhatsApp, videoconferência e troca segura de documentos."},
        {"q": "O atendimento é sigiloso?", "a": "Sim. O sigilo profissional é dever do advogado e direito do cliente. Tudo o que você compartilha fica protegido pela confidencialidade prevista no Estatuto da Advocacia."},
        {"q": "Como começamos?", "a": "Agende sua consulta pelo <a href=\"" + WA + "\" target=\"_blank\">WhatsApp</a>. Você conta o que aconteceu, analisamos com calma e retornamos com um diagnóstico claro e os próximos passos."}
    ]
}

data['contato'] = {
    "slug": "contato", "nav": "contato", "related_category": None,
    "page_title": "Contato · João Rocha Advocacia · OAB/UF 000.000",
    "page_description": "Fale com João Rocha Advocacia. Agende sua consulta pelo WhatsApp. Atendimento em Direito Criminal, Cível e Previdenciário, presencial e online em todo o Brasil.",
    "eyebrow": "Contato",
    "h1": "Vamos <em>conversar</em>.",
    "subtitle": "Agende sua consulta pelo WhatsApp. Conte o que aconteceu — analisamos com calma e retornamos com um diagnóstico claro.",
    "cta_text": "WhatsApp · (00) 00000-0000",
    "wa_text": "Olá, João Rocha. Vim pela página de contato.",
    "intro": {
        "h2": "Dois caminhos <em>para começar</em>.",
        "paragraphs": [
            "<strong>WhatsApp</strong> · o canal mais rápido para agendar sua consulta e enviar documentos. <a href=\"" + WA + "\" target=\"_blank\">(00) 00000-0000</a>",
            "<strong>Atendimento online</strong> · análise do caso, reuniões e acompanhamento por WhatsApp e videoconferência, em todo o Brasil.",
            "<strong>Presencial</strong> · com agendamento prévio · Sua Rua, 000 · Seu Bairro · Sua Cidade/UF"
        ]
    },
    "bullets_eye": "Como atendemos",
    "bullets_h2": "Atendimento <em>presencial e online</em>.",
    "bullets": [
        {"title": "Online em todo o Brasil", "text": "Análise inicial, reuniões e acompanhamento por WhatsApp e videoconferência. Documentos trocados por PDF com confidencialidade."},
        {"title": "Presencial com hora marcada", "text": "Atendimento no escritório mediante agendamento prévio, em horário comercial."},
        {"title": "Atendimento ágil", "text": "Você conta o que aconteceu e retornamos com um diagnóstico técnico e a indicação dos próximos passos."},
        {"title": "Sigilo profissional", "text": "Tudo que é compartilhado fica entre você e o escritório, com a obrigação de confidencialidade do Estatuto da Advocacia."}
    ],
    "faq": [
        {"q": "Como agendo uma consulta?", "a": "Basta chamar pelo <a href=\"" + WA + "\" target=\"_blank\">WhatsApp</a>. Você conta o que aconteceu, combinamos o melhor horário e seguimos com a análise do seu caso."},
        {"q": "Atendem quem mora em outra cidade?", "a": "Sim. Atendemos <strong>online em todo o Brasil</strong> por WhatsApp e videoconferência, com a mesma qualidade do atendimento presencial."},
        {"q": "Posso enviar documentos pelo WhatsApp?", "a": "Sim. Aceitamos PDF, foto e áudio. Para casos com muitos documentos, organizamos um link seguro de envio."},
        {"q": "Como funciona a primeira consulta?", "a": "Você expõe o seu caso pelo WhatsApp ou em videoconferência e recebe um diagnóstico inicial. A proposta de honorários é apresentada por escrito antes de qualquer trabalho."}
    ]
}

OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print('landings-content.json escrito com', len(data), 'paginas:', list(data.keys()))
