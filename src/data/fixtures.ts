import type { Activity, Ballot, Member, Section } from '../domain/types.js';
/** 100% synthetic content. No personal records from the WhatsApp export. */
export const sections: Section[] = [
  {id:'integridade',name:'Comitê de Integridade Institucional Academy'},
  {id:'representantes',name:'Conselho de Coligado de Representantes'},
  {id:'desenvolvimento',name:'Diretoria de Desenvolvimentos Institucional Academy'},
  {id:'coordenacao',name:'Coordenação Institucional Academy'},
  {id:'membros',name:'Membros Institucionais Academy'},
];
export const members: Member[] = [
  {id:'m01',acdmId:'DEMO-0001',name:'Helena Avelar',subtitle:'Conselharia de Integridade',totalVotes:80,proposals:12,approved:6,collaborations:35,sectionIds:['coordenacao'],role:'diretor'},
  {id:'m02',acdmId:'DEMO-0002',name:'Caio Martins',subtitle:'Representação institucional',totalVotes:24,proposals:12,approved:6,collaborations:19,sectionIds:['coordenacao'],role:'membro'},
  {id:'m03',acdmId:'DEMO-0003',name:'Lia Batista',subtitle:'Coordenação Academy',totalVotes:80,proposals:22,approved:14,collaborations:35,sectionIds:['coordenacao'],role:'membro'},
  {id:'m04',acdmId:'DEMO-0004',name:'Bruno Leal',subtitle:'Equipe institucional',totalVotes:84,proposals:10,approved:6,collaborations:16,sectionIds:['coordenacao','integridade'],role:'membro'},
  {id:'m05',acdmId:'DEMO-0005',name:'Sara Monteiro',subtitle:'Equipe institucional',totalVotes:77,proposals:20,approved:10,collaborations:40,sectionIds:['coordenacao'],role:'membro'},
  {id:'m06',acdmId:'DEMO-0006',name:'Daniel Freitas',subtitle:'Equipe institucional',totalVotes:148,proposals:37,approved:25,collaborations:21,sectionIds:['representantes'],role:'membro'},
  {id:'m07',acdmId:'DEMO-0007',name:'Mila Torres',subtitle:'Equipe institucional',totalVotes:89,proposals:16,approved:9,collaborations:27,sectionIds:['desenvolvimento'],role:'membro'},
];
export const ballots: Ballot[] = [
  {id:'b1',title:'Votação de objetos',section:'Comitê de Integridade Institucional Academy',description:'Descrição da votação e dos objetos. Conteúdo ilustrativo da prévia, aguardando o texto final da Academy.',status:'encerrada',options:[{id:'o1',label:'Objeto 01',votes:80},{id:'o2',label:'Objeto 02',votes:20}]},
];
const proposalSummary = 'Proposta ilustrativa de revisão do calendário de encontros, com etapas mais claras para a discussão e o acompanhamento das decisões.';
export const activities: Activity[] = [
  {id:'a1',memberId:'m01',type:'voto',title:'Título da votação',section:'Seção: Integridade Academy',code:'SCC-004 · 24/10/26',summary:'Social: Equipe Institucional Exemplo',approved:true,votes:56,percentage:74},
  {id:'a2',memberId:'m01',type:'voto',title:'Título da votação',section:'Seção: Conjunto Literário Institucional Academy',code:'SCC-003 · 20/10/26',summary:'Social: Equipe Institucional Exemplo',approved:false,votes:58,percentage:32},
  {id:'a3',memberId:'m01',type:'voto',title:'Título da votação',section:'Seção: Integridade Academy',code:'SCC-002 · 19/10/26',summary:'Social: Equipe Institucional Exemplo',approved:true,votes:58,percentage:57},
  {id:'a4',memberId:'m01',type:'proposicao',title:'Título da proposição',section:'Seção: Integridade Academy',code:'SCC-004 · 24/10/26',summary:proposalSummary,approved:true,votes:56,percentage:74},
  {id:'a5',memberId:'m01',type:'proposicao',title:'Título da proposição',section:'Seção: Conselho Academy',code:'SCC-003 · 20/10/26',summary:'Ajuste fictício nas orientações de participação, com registro público das deliberações e prazo para contribuições.',approved:false,votes:44,percentage:37},
  {id:'a6',memberId:'m01',type:'proposicao',title:'Título da proposição',section:'Seção: Integridade Academy',code:'SCC-002 · 19/10/26',summary:'Organização de um procedimento interno para revisar documentos e acompanhar respostas a propostas recebidas.',approved:true,votes:58,percentage:74},
];

// Small synthetic records for each profile; ensures the preview never opens on an empty demonstration.
const samples = [
 ['m02','Revisão do regimento', 'voto', true, 38, 69],
 ['m02','Proposta de calendário', 'proposicao', true, 23, 62],
 ['m03','Consulta de representatividade', 'voto', false, 19, 32],
 ['m03','Ajustes no regimento', 'proposicao', true, 33, 71],
 ['m04','Consulta de prioridades', 'voto', true, 55, 84],
 ['m04','Revisão de procedimentos', 'proposicao', false, 17, 29],
 ['m05','Consulta de comunicação', 'voto', true, 41, 73],
 ['m05','Plano de reuniões', 'proposicao', true, 30, 64],
 ['m06','Pauta de representação', 'voto', false, 22, 38],
 ['m06','Ciclo de propostas', 'proposicao', true, 46, 79],
 ['m07','Consulta de atividades', 'voto', true, 61, 91],
 ['m07','Proposta de colaboração', 'proposicao', false, 14, 27],
] as const;
for (const [memberId, title, type, approved, votes, percentage] of samples) {
 activities.push({
  id:`a-${memberId}-${type}`, memberId, type, title, section:'Seção: Cúpula Institucional Academy',
  code:'SIM-2026 · DEMO', summary:type==='voto'?'Consulta ilustrativa, sem dados institucionais reais.':proposalSummary,
  approved, votes, percentage,
 });
}

// A few extra records make the visual walkthrough useful on different member profiles.
// They remain independent of any actual institutional activity.
const extraProposals = [
  ['Revisão de calendário', 'Consulta simulada para adequar o calendário de reuniões às etapas previstas pela equipe.'],
  ['Acompanhamento de propostas', 'Modelo ilustrativo de registro das alterações propostas e das decisões tomadas em cada reunião.'],
] as const;
for (const member of members) {
  for (const [index, item] of extraProposals.entries()) {
    activities.push({id:`extra-${member.id}-${index}`,memberId:member.id,type:'proposicao',title:item[0],
      section:'Seção: Cúpula Institucional Academy',code:`DEMO-00${index+1} · 2026`,summary:item[1],
      approved:index===0,votes:index===0?41:23,percentage:index===0?72:39});
  }
}
