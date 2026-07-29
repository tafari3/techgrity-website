'use strict';

const digitalCapabilities = [
  {
    slug: 'software-ai-applications',
    title: 'Software, AI & Enterprise Applications',
    navTitle: 'Software, AI & Applications',
    description: 'Custom software, governed AI, web and mobile applications, enterprise platforms and institutional systems.',
    hero: 'Software and governed intelligence designed around real operations.',
    heroAccent: 'real operational work',
    scope: ['Custom operational software', 'Enterprise and institutional platforms', 'Web and mobile applications', 'Governed AI assistance and automation', 'System modernisation and phased replacement', 'Application maintenance and controlled change'],
    deliverables: ['User and stakeholder journeys', 'Solution and application architecture', 'Role-based workflows and interfaces', 'Integration and data contracts', 'Testing and acceptance evidence', 'Deployment, training and operating documentation'],
    approach: ['Discover users, responsibilities and operating constraints', 'Design journeys, controls, data and architecture', 'Build reviewable capability in controlled increments', 'Integrate identity, data and external services', 'Validate with users and technical acceptance criteria', 'Commission with migration, training and handover'],
    integrations: ['Identity and access', 'APIs and external platforms', 'Data platforms and reporting', 'Notifications and communications', 'Networks, hosting and backup'],
    industries: ['Government & Public Sector', 'Education & Research', 'Commerce, Logistics & Growing Organisations']
  },
  {
    slug: 'automation',
    title: 'Workflow & Process Automation',
    description: 'Digitise approvals, task routing, evidence, notifications, escalations and audit trails through controlled workflow automation.',
    hero: 'Move work through clear responsibilities, decisions and evidence.',
    heroAccent: 'decisions and evidence',
    scope: ['Process discovery and mapping', 'Digital forms and controlled intake', 'Approval and decision routing', 'Task, escalation and exception handling', 'Notifications and reminders', 'Evidence, audit trails and reporting'],
    deliverables: ['Current-state and future-state process maps', 'Role and approval matrix', 'Workflow configuration or software', 'Notification and escalation rules', 'Audit and evidence model', 'User guidance and support controls'],
    approach: ['Identify delays and accountability gaps', 'Define roles, decisions and evidence', 'Design the controlled future workflow', 'Implement and integrate required systems', 'Pilot with real users and scenarios', 'Commission with monitoring and improvement'],
    integrations: ['Email and messaging', 'Identity and access', 'Enterprise applications', 'Document and data services', 'Reporting and dashboards'],
    industries: ['Government & Public Sector', 'Energy, Utilities & Industrial Operations', 'Commerce, Logistics & Growing Organisations']
  },
  {
    slug: 'integration',
    title: 'Systems Integration',
    description: 'Connect applications, APIs, identity services, legacy systems and data exchanges through governed systems integration.',
    hero: 'Connect systems without losing control of identity, data or responsibility.',
    heroAccent: 'identity, data or responsibility',
    scope: ['API design and integration', 'Legacy-system connectivity', 'Identity and single sign-on integration', 'Event and message exchange', 'Data synchronisation and migration', 'Integration monitoring and failure handling'],
    deliverables: ['Integration architecture', 'Interface and data contracts', 'Authentication and authorisation design', 'Transformation and validation rules', 'Operational monitoring and runbooks', 'Integration test evidence'],
    approach: ['Inventory systems and ownership', 'Define authoritative data and interfaces', 'Design security and failure behaviour', 'Build in controlled environments', 'Test normal, edge and recovery scenarios', 'Commission with monitoring and support'],
    integrations: ['APIs and webhooks', 'Databases and data platforms', 'Identity providers', 'Messaging and event systems', 'On-premise and cloud environments'],
    industries: ['Data Centres & Technology Organisations', 'Telecommunications', 'Government & Public Sector']
  },
  {
    slug: 'data-analytics',
    title: 'Data Platforms & Analytics',
    description: 'Design data architecture, integration, dashboards, reporting, governance and decision-support platforms for operational visibility.',
    hero: 'Turn operational data into trusted visibility and accountable decisions.',
    heroAccent: 'trusted visibility and accountable decisions',
    scope: ['Data architecture and modelling', 'Collection and integration pipelines', 'Data quality and governance', 'Operational dashboards and reporting', 'Alerts and decision support', 'Secure analytical access'],
    deliverables: ['Data inventory and ownership model', 'Architecture and integration design', 'Validated data pipelines', 'Dashboards and reports', 'Quality, retention and access controls', 'Monitoring and operating documentation'],
    approach: ['Define decisions and information needs', 'Identify sources, ownership and quality risks', 'Design governed data flows', 'Implement ingestion, storage and reporting', 'Validate meaning and accuracy with users', 'Commission with monitoring and stewardship'],
    integrations: ['Operational applications', 'Databases and files', 'Sensors and field systems', 'Identity and access', 'Business intelligence tools'],
    industries: ['Energy, Utilities & Industrial Operations', 'Telecommunications', 'Education & Research']
  },
  {
    slug: 'cybersecurity-access',
    title: 'Cybersecurity & Digital Access',
    description: 'Strengthen identity, authentication, role-based access, auditability and security-conscious implementation across digital systems.',
    hero: 'Make access, responsibility and evidence part of the system design.',
    heroAccent: 'part of the system design',
    scope: ['Identity and access architecture', 'Authentication and multi-factor readiness', 'Role and permission design', 'Privileged access controls', 'Audit and activity evidence', 'Secure implementation and review'],
    deliverables: ['Identity and role model', 'Access-control matrix', 'Authentication and session design', 'Security configuration baseline', 'Audit and evidence requirements', 'Operational access procedures'],
    approach: ['Identify users, assets and trust boundaries', 'Define roles and separation of duties', 'Design authentication and recovery controls', 'Implement with least-privilege defaults', 'Test access and abuse scenarios', 'Commission with ownership and review cycles'],
    integrations: ['Identity providers', 'Applications and APIs', 'Physical access systems', 'Logging and monitoring', 'Networks and infrastructure'],
    industries: ['Government & Public Sector', 'Data Centres & Technology Organisations', 'Education & Research']
  }
];

const infrastructureCapabilities = [
  {
    slug: 'networks-fibre', title: 'Networks & Fibre', description: 'Design and implement enterprise networks, fibre-optic infrastructure, structured cabling, wireless connectivity and network monitoring.', hero: 'Connectivity designed around coverage, capacity, resilience and support.',
    heroAccent: 'coverage, capacity, resilience and support',
    scope: ['Enterprise LAN and WAN', 'Fibre-optic infrastructure', 'Structured cabling', 'Wireless and microwave connectivity', 'Network monitoring and optimisation', 'Network security foundations'],
    deliverables: ['Site and network assessment', 'Logical and physical design', 'Equipment and bill of materials', 'Installation and configuration', 'Testing and labelling evidence', 'As-built documentation and support plan'],
    approach: ['Assess sites and current network', 'Model capacity, coverage and resilience', 'Specify topology and equipment', 'Install and configure under change control', 'Test performance, failover and security', 'Handover with records and support'],
    integrations: ['Data centres and cloud', 'Telecom and radio', 'Security and smart facilities', 'Power and monitoring'],
    industries: ['Education & Research', 'Government & Public Sector', 'Data Centres & Technology Organisations']
  },
  {
    slug: 'data-centres-cloud', title: 'Data Centres & Cloud', description: 'Plan and integrate data-centre environments, servers, storage, virtualisation, backup, monitoring and hybrid cloud infrastructure.', hero: 'Compute, storage and resilience designed as one operating environment.',
    heroAccent: 'one operating environment',
    scope: ['Server and technical-room planning', 'Compute, storage and virtualisation', 'Backup and recovery architecture', 'Hybrid cloud integration', 'Monitoring and capacity management', 'Network, power and environmental integration'],
    deliverables: ['Environment and workload assessment', 'Architecture and capacity design', 'Equipment and licensing schedule', 'Build and migration plan', 'Resilience and recovery tests', 'As-built and operating documentation'],
    approach: ['Assess workloads and current environment', 'Design compute, storage, network and recovery layers', 'Specify infrastructure and dependencies', 'Build and migrate in controlled stages', 'Test performance, backup and recovery', 'Commission with monitoring and ownership'],
    integrations: ['Networks and fibre', 'Power and energy', 'Security and access', 'Digital systems and data platforms'],
    industries: ['Data Centres & Technology Organisations', 'Education & Research', 'Government & Public Sector']
  },
  {
    slug: 'telecom-radio', title: 'Telecom & Radio Infrastructure', description: 'Deliver telecom, radio, microwave, backhaul, tower and base-station infrastructure with integration and commissioning controls.', hero: 'Communications infrastructure coordinated from site requirement to commissioned service.',
    heroAccent: 'commissioned service',
    scope: ['Radio and microwave systems', 'Backhaul and transmission', 'Tower and antenna infrastructure', 'Base-station and site integration', 'Equipment shelters and technical rooms', 'Site power, monitoring and commissioning'],
    deliverables: ['Site and path assessment', 'Radio or transmission design', 'Equipment and installation schedule', 'Site integration and configuration', 'Alignment and commissioning evidence', 'As-built records and maintenance plan'],
    approach: ['Assess service, site and path conditions', 'Design access, backhaul, power and monitoring', 'Coordinate equipment and specialist works', 'Install and integrate the site', 'Test alignment, quality and resilience', 'Commission with evidence and support'],
    integrations: ['Networks and fibre', 'Power and energy', 'Civil and technical works', 'Monitoring and field workflows'],
    industries: ['Telecommunications', 'Energy, Utilities & Industrial Operations', 'Government & Public Sector']
  },
  {
    slug: 'power-energy', title: 'Power & Energy Systems', description: 'Improve technology resilience with UPS, backup power, solar, batteries, hybrid energy, distribution and power monitoring solutions.', hero: 'Power resilience designed around the load, service and operating environment.',
    heroAccent: 'critical technology operation',
    scope: ['Load and power-quality assessment', 'UPS and backup power', 'Solar and battery systems', 'Hybrid energy design', 'Distribution and protection', 'Power monitoring and alerting'],
    deliverables: ['Load profile and resilience requirement', 'Power architecture and sizing', 'Equipment and protection schedule', 'Installation and integration', 'Runtime, failover and safety tests', 'Operating and maintenance documentation'],
    approach: ['Assess loads and outage risks', 'Define autonomy and resilience targets', 'Design source, storage and protection layers', 'Install and integrate with technical systems', 'Test failover, runtime and monitoring', 'Commission with maintenance ownership'],
    integrations: ['Data centres', 'Telecom sites', 'Networks and security', 'Technical facilities and monitoring'],
    industries: ['Telecommunications', 'Energy, Utilities & Industrial Operations', 'Data Centres & Technology Organisations']
  },
  {
    slug: 'security-smart-facilities', title: 'Security & Smart Facilities', description: 'Integrate CCTV, physical access control, monitoring, sensors, alarms and smart-facility systems with operational technology.', hero: 'Physical security and facility visibility connected to accountable operations.',
    heroAccent: 'one controlled environment',
    scope: ['CCTV and video management', 'Physical access control', 'Intrusion and alarm systems', 'Sensors and environmental monitoring', 'Control-room and operator interfaces', 'Digital identity and event integration'],
    deliverables: ['Risk and coverage assessment', 'Camera, access and sensor design', 'Equipment and retention schedule', 'Installation and configuration', 'Coverage and event-response tests', 'Operating procedures and support records'],
    approach: ['Assess assets, spaces and responsibilities', 'Define coverage, retention and access rules', 'Design physical and digital integration', 'Install and configure under privacy controls', 'Test detection, response and evidence', 'Commission with operator training'],
    integrations: ['Digital identity', 'Networks and storage', 'Power and resilience', 'Monitoring and workflow systems'],
    industries: ['Government & Public Sector', 'Education & Research', 'Commerce, Logistics & Growing Organisations']
  },
  {
    slug: 'civil-technical-works', title: 'Civil & Technical Infrastructure', description: 'Coordinate technical rooms, equipment shelters, foundations, pathways, mounting structures, site preparation and controlled fit-outs.', hero: 'Technical enabling works designed around the systems they must support.',
    heroAccent: 'the systems they must support',
    scope: ['Technical rooms and controlled fit-outs', 'Equipment shelters and enclosures', 'Cable pathways and containment', 'Foundations and mounting structures', 'Site preparation and access', 'Specialist coordination and technical handover'],
    deliverables: ['Site and technical requirement assessment', 'Layout and enabling-work specification', 'Quantities and specialist responsibilities', 'Controlled implementation', 'Inspection and acceptance evidence', 'As-built records and maintenance notes'],
    approach: ['Confirm technical equipment and site constraints', 'Define interfaces and specialist responsibilities', 'Design enabling works and quantities', 'Coordinate implementation and quality checks', 'Inspect against technical acceptance needs', 'Handover as part of the integrated system'],
    integrations: ['Telecom and radio', 'Networks and fibre', 'Power and energy', 'Security and smart facilities'],
    industries: ['Telecommunications', 'Energy, Utilities & Industrial Operations', 'Data Centres & Technology Organisations']
  }
];

const industries = [
  {slug:'government-public-sector', title:'Government & Public Sector', description:'Accountable digital platforms, secure networks, data-centre infrastructure, communications, access control and power resilience.', hero:'Technology for public services that must remain accountable, secure and supportable.', priorities:['Service accessibility and continuity','Clear institutional responsibilities','Security, privacy and auditability','Procurement and acceptance evidence','Long-term operating support'], digital:['Citizen and institutional portals','Case, service and approval workflows','Identity, permissions and audit trails','Data integration, reporting and decision support'], infrastructure:['Secure networks and connectivity','Data-centre and hybrid infrastructure','Communications and field connectivity','Access control, monitoring and resilient power'], patterns:['Integrated public-service platform','Secure institutional network and data environment','Field-service workflow with communications and evidence'], controls:['Stakeholder and responsibility mapping','Security and privacy by design','Testing against agreed acceptance criteria','Documentation, training and handover']},
  {slug:'education-research', title:'Education & Research', description:'Institutional platforms, campus networks, learning systems, research computing, access control and resilient infrastructure.', hero:'Connect learning, administration, research and campus infrastructure as one institutional environment.', priorities:['Reliable campus and remote access','Institutional data and workflow integrity','Learning and research continuity','Role-based access and support','Scalable infrastructure'], digital:['Student and institutional platforms','Learning and research workflows','Data integration and analytics','Identity and secure digital access'], infrastructure:['Campus networks and fibre','Research compute and storage','Data-centre and cloud integration','Access control, monitoring and backup power'], patterns:['Integrated university operating platform','Campus network and data-centre renewal','Research-computing environment with governed access'], controls:['User and academic stakeholder validation','Data ownership and migration planning','Capacity and resilience testing','Documentation and knowledge transfer']},
  {slug:'telecommunications', title:'Telecommunications', description:'Network infrastructure, radio and microwave systems, site power, field workflows and monitoring platforms.', hero:'Connect communications infrastructure, field work and operational visibility.', priorities:['Coverage, capacity and service quality','Field-site resilience and maintainability','Controlled configuration and change','Commissioning evidence','Operational monitoring'], digital:['Field-work and site-management workflows','Asset, fault and maintenance platforms','Operational dashboards and alerts','Integration with network and business systems'], infrastructure:['Radio, microwave and backhaul','Tower and site infrastructure','Fibre and network connectivity','Site power, shelters, security and monitoring'], patterns:['Connected telecom site and field workflow','Backhaul and site-power upgrade','Network operations data and maintenance platform'], controls:['Site and path assessment','Specialist responsibility coordination','Alignment, resilience and acceptance tests','As-built and maintenance records']},
  {slug:'energy-utilities-industrial', title:'Energy, Utilities & Industrial Operations', description:'Operational platforms, field workflows, connectivity, communications, monitoring, power resilience and technical facilities.', hero:'Technology for distributed operations where field evidence and continuity matter.', priorities:['Field visibility and accountability','Reliable remote connectivity','Operational and safety controls','Asset and maintenance evidence','Resilient technical environments'], digital:['Field-work and inspection workflows','Asset and maintenance platforms','Data collection, dashboards and alerts','Integration with operational and business systems'], infrastructure:['Industrial and remote connectivity','Radio, fibre and network infrastructure','Monitoring, security and technical rooms','Power resilience for critical technology'], patterns:['Field operations and evidence platform','Remote-site connectivity and monitoring','Integrated asset, maintenance and reporting environment'], controls:['Operating and safety requirement discovery','Environment-specific technical design','Recovery and failure-mode testing','Controlled handover and support']},
  {slug:'data-centres-technology', title:'Data Centres & Technology Organisations', description:'Compute, storage, virtualisation, networks, power, monitoring, security, technical rooms and operational platforms.', hero:'Build the operational layers technology organisations depend on every day.', priorities:['Availability and recoverability','Capacity and performance visibility','Secure access and change control','Power and environmental resilience','Documented operational ownership'], digital:['Operations and service-management workflows','Monitoring, dashboards and alerts','Identity and privileged access','Integration, inventory and reporting'], infrastructure:['Compute, storage and virtualisation','Networks and hybrid connectivity','Backup and recovery infrastructure','Power, cooling, security and technical facilities'], patterns:['Data-centre environment renewal','Hybrid infrastructure and recovery architecture','Operational control and monitoring platform'], controls:['Workload and dependency assessment','Capacity and resilience design','Migration and recovery testing','Configuration and as-built records']},
  {slug:'commerce-logistics-growing-organisations', title:'Commerce, Logistics & Growing Organisations', description:'Software, mobile workflows, integration, connectivity, security, data visibility, power resilience and support.', hero:'Scale operations without losing visibility, control or service continuity.', priorities:['Efficient customer and operational workflows','Distributed visibility and coordination','Reliable connectivity and devices','Security and role clarity','Scalable support'], digital:['Operational and customer applications','Mobile and distributed workflows','Systems and data integration','Dashboards, alerts and reporting'], infrastructure:['Branch and site connectivity','Cloud and hosting infrastructure','Security and access control','Backup power and monitoring'], patterns:['Mobile logistics and evidence workflow','Integrated commerce operations platform','Distributed branch connectivity and security'], controls:['Process and growth requirement discovery','Phased implementation and integration','User validation and operating evidence','Support and continuous improvement']}
];

const metadata = {
  home: {title:'Techgrity Systems | Digital Systems & Critical Infrastructure', description:'Techgrity Systems designs and integrates software, AI, networks, data centres, telecommunications, power and technical infrastructure.'},
  capabilities: {title:'Technology Capabilities | Techgrity Systems', description:'Explore Techgrity capabilities across software, AI, automation, networks, fibre, data centres, telecoms, power and technical infrastructure.'},
  industries: {title:'Industries We Support | Techgrity Systems', description:'See how Techgrity combines digital systems and infrastructure for government, education, telecoms, energy, technology and commerce.'}
};

module.exports = { digitalCapabilities, infrastructureCapabilities, industries, metadata };
