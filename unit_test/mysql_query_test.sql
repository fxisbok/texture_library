use texture_library;
show databases;
select * from asset;

insert into asset (asset_name, asset_type) values ('tst_asset', 'tst');
select * from asset;

update asset set asset_type='TEST' where asset_name='tst_asset';
select * from asset;

delete from asset where asset_name='tst_asset';
select * from asset;

#-------------

drop table if exists asset;
show tables;

create table if not exists asset_metadata (
	id int auto_increment primary key,
    asset_name varchar(50) unique,
    resolution varchar(50),
    created_at timestamp default current_timestamp
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

create table if not exists asset_tag (
	id int auto_increment primary key not null,
    tag_name varchar(50) unique not null
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

create table if not exists asset_type (
	id int auto_increment primary key not null,
    type_name varchar(50) unique not null
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

create table if not exists assets (
	id int,
    asset_name varchar(50),
    asset_type varchar(50),
    asset_tag varchar(50),
    
    foreign key (id) references asset_metadata(id) on delete cascade,
    foreign key (asset_name) references asset_metadata(asset_name) on delete cascade
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

desc asset_metadata;
desc asset_tag;
desc asset_type;
desc assets;

#----------

insert into asset_metadata (asset_name, resolution) values ('test_asset', '512*512');
select * from asset_metadata;
select * from assets;

drop table assets;
drop table asset_metadata;

create table if not exists assets (
	id int auto_increment primary key,
    asset_name varchar(255) not null,
    asset_type_id int,
    asset_tag_id int,
    
    foreign key (asset_type_id) references asset_type(id) on delete set null,
    foreign key (asset_tag_id) references asset_tag(id) on delete set null
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

create table if not exists asset_metadata (
	id int primary key,
    resolution varchar(50),
    created_at timestamp default current_timestamp,
    file_path varchar(512),
    
    foreign key (id) references assets(id) on delete cascade
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

insert into assets (asset_name) values ('test_asset');
insert into asset_metadata (id, resolution, file_path) values (1, '512*512', '/path/to/test_asset');
delete from assets where id=1;

select * from asset_metadata;

# -----

alter table assets add column num_favorites int default 0;

delimiter //
create trigger on_insert_assets
after insert on assets
for each row
begin
	insert into asset_metadata (id, asset_name)
    values (new.id, new.asset_name);
end;
//
delimiter ;

insert into assets (asset_name) values ('test_asset');
select asset_name from assets; 
flush tables;

drop trigger if exists on_insert_assets;
insert into assets (asset_name) values ('test_asset_02');

delimiter //
create trigger after_insert_assets
	after insert on assets
    for each row
    BEGIN
		insert into asset_metadata (id) values (NEW.id);
	END;
// delimiter ;

insert into assets (asset_name) values ('test_asset_04');
commit;
select * from assets;
select * from texture_library.asset_metadata;

show triggers;

create table if not exists mapping_asset_tag (
	id int auto_increment primary key,
    asset_id int,
    tag_id int,
    
    foreign key (asset_id) references assets(id) on delete cascade,
    foreign key (tag_id) references asset_tag(id) on delete cascade
)  ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

show tables;

desc assets;