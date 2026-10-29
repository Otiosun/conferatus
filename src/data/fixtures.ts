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
  {id:'m08',acdmId:'DEMO-0008',name:'Rafael Vieira',subtitle:'Comitê de integridade',totalVotes:34,proposals:5,approved:2,collaborations:11,sectionIds:['integridade'],role:'diretor'},
  {id:'m09',acdmId:'DEMO-0009',name:'Olívia Campos',subtitle:'Conselho de representantes',totalVotes:41,proposals:6,approved:3,collaborations:13,sectionIds:['representantes'],role:'membro'},
  {id:'m10',acdmId:'DEMO-0010',name:'Pedro Nogueira',subtitle:'Desenvolvimento institucional',totalVotes:48,proposals:7,approved:4,collaborations:15,sectionIds:['desenvolvimento'],role:'diretor'},
  {id:'m11',acdmId:'DEMO-0011',name:'Vitor Almeida',subtitle:'Participação institucional',totalVotes:55,proposals:8,approved:5,collaborations:17,sectionIds:['desenvolvimento'],role:'membro'},
  {id:'m12',acdmId:'DEMO-0012',name:'Marina Duarte',subtitle:'Membro institucional',totalVotes:62,proposals:9,approved:6,collaborations:19,sectionIds:['membros'],role:'membro'},
  {id:'m13',acdmId:'DEMO-0013',name:'Thiago Reis',subtitle:'Membro institucional',totalVotes:69,proposals:10,approved:7,collaborations:21,sectionIds:['membros'],role:'membro'},
  {id:'m14',acdmId:'DEMO-0014',name:'Júlia Barreto',subtitle:'Membro institucional',totalVotes:76,proposals:11,approved:8,collaborations:23,sectionIds:['membros'],role:'membro'},
  {id:'m15',acdmId:'DEMO-0015',name:'Lucas Melo',subtitle:'Membro institucional',totalVotes:83,proposals:12,approved:9,collaborations:25,sectionIds:['membros'],role:'membro'},
  {id:'m16',acdmId:'DEMO-0016',name:'Ana Ferreira',subtitle:'Membro institucional',totalVotes:90,proposals:13,approved:10,collaborations:27,sectionIds:['membros'],role:'membro'},
];
export const ballots: Ballot[] = [
  {id:'b1',title:'Revisão do calendário de reuniões',section:'Comitê de Integridade Institucional Academy',description:'Escolha do modelo de calendário para os próximos encontros.',status:'aberta',options:[{id:'o1',label:'Calendário mensal',votes:80},{id:'o2',label:'Calendário quinzenal',votes:20}]},
];
const proposalSummary = 'Organização das datas de reunião, com antecedência para convocação e registro das decisões.';
export const activities: Activity[] = [
  {id:'a1',memberId:'m01',type:'voto',title:'Revisão do calendário de reuniões',section:'Seção: Integridade Academy',code:'SCC-004 · 24/10/26',summary:'Participação registrada na consulta sobre o calendário.',approved:true,votes:56,percentage:74},
  {id:'a2',memberId:'m01',type:'voto',title:'Revisão do calendário de reuniões',section:'Seção: Conjunto Literário Institucional Academy',code:'SCC-003 · 20/10/26',summary:'Participação registrada na consulta sobre o calendário.',approved:false,votes:58,percentage:32},
  {id:'a3',memberId:'m01',type:'voto',title:'Revisão do calendário de reuniões',section:'Seção: Integridade Academy',code:'SCC-002 · 19/10/26',summary:'Participação registrada na consulta sobre o calendário.',approved:true,votes:58,percentage:57},
  {id:'a4',memberId:'m01',type:'proposicao',title:'Atualização do calendário institucional',section:'Seção: Integridade Academy',code:'SCC-004 · 24/10/26',summary:proposalSummary,approved:true,votes:56,percentage:74},
  {id:'a5',memberId:'m01',type:'proposicao',title:'Atualização do calendário institucional',section:'Seção: Conselho Academy',code:'SCC-003 · 20/10/26',summary:'Definição de prazos para contribuições e registro das decisões nas atas.',approved:false,votes:44,percentage:37},
  {id:'a6',memberId:'m01',type:'proposicao',title:'Atualização do calendário institucional',section:'Seção: Integridade Academy',code:'SCC-002 · 19/10/26',summary:'Organização de um procedimento interno para revisar documentos e acompanhar respostas a propostas recebidas.',approved:true,votes:58,percentage:74},
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
 ['m08','Consulta de calendário','voto',true,16,53],
 ['m09','Consulta de calendário','voto',true,19,54],
 ['m10','Consulta de calendário','voto',true,22,55],
 ['m11','Consulta de calendário','voto',true,25,56],
 ['m12','Consulta de calendário','voto',true,28,57],
 ['m13','Consulta de calendário','voto',true,31,58],
 ['m14','Consulta de calendário','voto',true,34,59],
 ['m15','Consulta de calendário','voto',true,37,60],
 ['m16','Consulta de calendário','voto',true,40,61],
] as const;
for (const [memberId, title, type, approved, votes, percentage] of samples) {
 activities.push({
  id:`a-${memberId}-${type}`, memberId, type, title, section:'Seção: Cúpula Institucional Academy',
  code:'SIM-2026 · DEMO', summary:type==='voto'?'Participação registrada nesta consulta.':proposalSummary,
  approved, votes, percentage,
 });
}

// A few extra records make the visual walkthrough useful on different member profiles.
// They remain independent of any actual institutional activity.
const extraProposals = [
  ['Revisão de calendário', 'Organização das datas de reunião e do período de análise das propostas.'],
  ['Acompanhamento de propostas', 'Registro das propostas recebidas, alterações aprovadas e decisões finais.'],
] as const;
for (const member of members) {
  for (const [index, item] of extraProposals.entries()) {
    activities.push({id:`extra-${member.id}-${index}`,memberId:member.id,type:'proposicao',title:item[0],
      section:'Seção: Cúpula Institucional Academy',code:`DEMO-00${index+1} · 2026`,summary:item[1],
      approved:index===0,votes:index===0?41:23,percentage:index===0?72:39});
  }
}
