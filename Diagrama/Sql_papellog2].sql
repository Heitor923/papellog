create database papellog3;
use papellog3;
create table usuarios (
id int not null auto_increment,
username varchar(50) not null,
nome varchar(100) not null,
email varchar(150) not null,
senha_hash varchar(255) not null,
perfil enum('ADMIN','FUNCIONARIO') not null,
ativo boolean not null default true,
constraint pk_usuarios primary key (id),
constraint uq_usuarios_username unique (username),
constraint uq_usuarios_email unique (email)
);
create table clientes (
id int not null auto_increment,
cpf char(11) not null,
nome varchar(100) not null,
email varchar(150) null,
telefone varchar(20) null,
endereco varchar(255) null,
constraint pk_clientes primary key (id),
constraint uq_clientes_cpf unique (cpf),
constraint uq_clientes_email unique (email)
);
create table produtos (
id int not null auto_increment,
nome varchar(150) not null,
sku varchar(50) not null,
preco decimal(10,2) not null,
estoque_atual int not null default 0,
estoque_minimo int not null default 0,
ativo boolean not null default true,
constraint pk_produtos primary key (id),
constraint uq_produtos_sku unique (sku),
constraint ck_produtos_preco check (preco >= 0),
constraint ck_estoque_atual check (estoque_atual >= 0),
constraint ck_estoque_minimo check (estoque_minimo >= 0)
);
create table vendas (
id int not null auto_increment,
cliente_id int not null,
usuario_id int not null,
data_venda datetime not null default current_timestamp,
total decimal(10,2) not null,
status_venda enum('PENDENTE','FINALIZADA','CANCELADA') not null default 'PENDENTE',
constraint pk_vendas primary key (id),
constraint ck_vendas_total check (total >= 0)
);
alter table vendas
add constraint fk_vendas_cliente foreign key (cliente_id)
references clientes (id)
on delete restrict on update cascade;
alter table vendas
add constraint fk_vendas_usuario foreign key (usuario_id)
references usuarios (id)
on delete restrict on update cascade;
create table itens_venda (
id int not null auto_increment,
venda_id int not null,
produto_id int not null,
quantidade int not null,
preco_unitario decimal(10,2) not null,
subtotal decimal(10,2) not null,
constraint pk_itens_venda primary key (id),
constraint ck_itens_quantidade check (quantidade > 0),
constraint ck_itens_preco_unitario check (preco_unitario >= 0),
constraint ck_itens_subtotal check (subtotal >= 0)
);
alter table itens_venda
add constraint fk_itens_venda foreign key (venda_id)
references vendas (id)
on delete cascade on update cascade;
alter table itens_venda
add constraint fk_itens_produto foreign key (produto_id)
references produtos (id)
on delete restrict on update cascade;
create table relatorios_venda (
id int not null auto_increment,
cliente_id int null,
data_inicio date not null,
data_fim date not null,
gerado_em datetime not null default current_timestamp,
constraint pk_relatorios primary key (id),
constraint ck_relatorios_periodo check (data_fim >= data_inicio)
);
alter table relatorios_venda
add constraint fk_relatorios_cliente foreign key (cliente_id)
references clientes (id)
on delete set null on update cascade;
