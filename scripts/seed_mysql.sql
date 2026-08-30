-- Seed coerente (MySQL). Executar o arquivo inteiro.
-- user_id = login = CPF. Senha = iniciais + 4 ultimos digitos do CPF.
--
-- Staff:
--   39053344705 Jose Mecanico      Mecanico     JM4705
--   85351346893 Pedro Paulo        Mecanico     PP6893
--   10000000019 Ana Atendente      Atendente    AA0019
--   11144477735 Carlos Estoquista  Estoquista   CE7735
--   71428793860 Bruno Comprador    Comprador    BC3860
-- Clientes:
--   52998224725 Andrey Murari      AM4725  Civic ABC1D23
--   10000000108 Maria Silva        MS0108  Onix  DEF2A34
--   10000000361 Joao Santos        JS0361  Gol   GHI3B45
--   10000000442 Lucia Ferreira     LF0442  HB20  JKL4C56
--
-- Kits servico -> peca:
--   1 oleo            -> oleo 5W30 + filtro de oleo
--   2 correia dentada -> correia + tensor
--   3 pastilha freio  -> pastilha dianteira
--   4 troca de pneu   -> pneu 185/60 R15 + bico
--   5 alinhamento     -> contrapeso
--   6 arrefecimento   -> aditivo + tampa do reservatorio

START TRANSACTION;

INSERT INTO `user` (
    user_id, user_type, login, password,
    user_modification_id, flag_active, insertion_date, modification_date
) VALUES
    ('39053344705', 'Mecânico',   '39053344705', 'JM4705', 1, TRUE, '2026-01-10 08:00:00', NULL),
    ('85351346893', 'Mecânico',   '85351346893', 'PP6893', 1, TRUE, '2026-01-10 08:00:00', NULL),
    ('10000000019', 'Atendente',  '10000000019', 'AA0019', 1, TRUE, '2026-01-10 08:00:00', NULL),
    ('11144477735', 'Estoquista', '11144477735', 'CE7735', 1, TRUE, '2026-01-10 08:00:00', NULL),
    ('71428793860', 'Comprador',  '71428793860', 'BC3860', 1, TRUE, '2026-01-10 08:00:00', NULL),
    ('52998224725', 'Cliente',    '52998224725', 'AM4725', 1, TRUE, '2026-01-12 09:00:00', NULL),
    ('10000000108', 'Cliente',    '10000000108', 'MS0108', 1, TRUE, '2026-01-12 09:00:00', NULL),
    ('10000000361', 'Cliente',    '10000000361', 'JS0361', 1, TRUE, '2026-01-12 09:00:00', NULL),
    ('10000000442', 'Cliente',    '10000000442', 'LF0442', 1, TRUE, '2026-01-12 09:00:00', NULL);

INSERT INTO person (
    person_id, complete_name, user_id, user_modification_id,
    flag_customer, flag_active, insertion_date, modification_date
) VALUES
    ('39053344705', 'Jose Mecanico',     '39053344705', 1, FALSE, TRUE, '2026-01-10 08:00:00', '2026-01-10 08:00:00'),
    ('85351346893', 'Pedro Paulo',       '85351346893', 1, FALSE, TRUE, '2026-01-10 08:00:00', '2026-01-10 08:00:00'),
    ('10000000019', 'Ana Atendente',     '10000000019', 1, FALSE, TRUE, '2026-01-10 08:00:00', '2026-01-10 08:00:00'),
    ('11144477735', 'Carlos Estoquista', '11144477735', 1, FALSE, TRUE, '2026-01-10 08:00:00', '2026-01-10 08:00:00'),
    ('71428793860', 'Bruno Comprador',   '71428793860', 1, FALSE, TRUE, '2026-01-10 08:00:00', '2026-01-10 08:00:00'),
    ('52998224725', 'Andrey Murari',     '52998224725', 1, TRUE,  TRUE, '2026-01-12 09:00:00', '2026-01-12 09:00:00'),
    ('10000000108', 'Maria Silva',       '10000000108', 1, TRUE,  TRUE, '2026-01-12 09:00:00', '2026-01-12 09:00:00'),
    ('10000000361', 'Joao Santos',       '10000000361', 1, TRUE,  TRUE, '2026-01-12 09:00:00', '2026-01-12 09:00:00'),
    ('10000000442', 'Lucia Ferreira',    '10000000442', 1, TRUE,  TRUE, '2026-01-12 09:00:00', '2026-01-12 09:00:00');

INSERT INTO address (
    cep_id, street, neighborhood, city, state,
    user_modification_id, flag_active, insertion_date, modification_date
) VALUES
    ('01001000', 'Praca da Se',        'Se',     'Sao Paulo',      'SP', 1, TRUE, '2026-01-12 09:00:00', NULL),
    ('05040000', 'Rua Guaicurus',      'Lapa',   'Sao Paulo',      'SP', 1, TRUE, '2026-01-12 09:00:00', NULL),
    ('30120010', 'Rua da Bahia',       'Centro', 'Belo Horizonte', 'MG', 1, TRUE, '2026-01-12 09:00:00', NULL),
    ('80010000', 'Rua XV de Novembro', 'Centro', 'Curitiba',       'PR', 1, TRUE, '2026-01-12 09:00:00', NULL);

INSERT INTO person_address (
    person_address_id, person_id, cep_id, number, complement,
    user_modification_id, flag_active, insertion_date, modification_date
) VALUES
    (1, '39053344705', '05040000', '50',  NULL,          1, TRUE, '2026-01-12 09:00:00', NULL),
    (2, '52998224725', '01001000', '176', 'APTO 2812 A', 1, TRUE, '2026-01-12 09:00:00', NULL),
    (3, '10000000108', '05040000', '200', NULL,          1, TRUE, '2026-01-12 09:00:00', NULL),
    (4, '10000000361', '30120010', '900', 'sala 12',     1, TRUE, '2026-01-12 09:00:00', NULL),
    (5, '10000000442', '80010000', '45',  NULL,          1, TRUE, '2026-01-12 09:00:00', NULL);

INSERT INTO person_contact (
    contact_id, person_id, contact_type, value, flag_preferred,
    user_modification_id, flag_active, insertion_date, modification_date
) VALUES
    (1, '39053344705', 'Celular',  '11988880001',          TRUE,  1, TRUE, '2026-01-12 09:00:00', NULL),
    (2, '85351346893', 'Celular',  '11988880002',          TRUE,  1, TRUE, '2026-01-12 09:00:00', NULL),
    (3, '10000000019', 'E-mail',   'ana@oficina.test',     TRUE,  1, TRUE, '2026-01-12 09:00:00', NULL),
    (4, '52998224725', 'Celular',  '11987654321',          TRUE,  1, TRUE, '2026-01-12 09:00:00', NULL),
    (5, '52998224725', 'E-mail',   'andrey@example.com',   FALSE, 1, TRUE, '2026-01-12 09:00:00', NULL),
    (6, '10000000108', 'WhatsApp', '11977770001',          TRUE,  1, TRUE, '2026-01-12 09:00:00', NULL),
    (7, '10000000361', 'Telefone', '3133334444',           TRUE,  1, TRUE, '2026-01-12 09:00:00', NULL),
    (8, '10000000442', 'Celular',  '41999990001',          TRUE,  1, TRUE, '2026-01-12 09:00:00', NULL);

INSERT INTO vehicle (
    vehicle_id, person_id, model, brand, manufacture_year, model_year,
    engine, fuel_type, plate, color, description,
    user_modification_id, flag_active, insertion_date, modification_date
) VALUES
    (1, '52998224725', 'Civic', 'Honda',     '2020', '2021', '2.0', 'Gasolina', 'ABC1D23', 'Prata',  'Carro do Andrey', 1, TRUE, '2026-01-13 10:00:00', NULL),
    (2, '10000000108', 'Onix',  'Chevrolet', '2019', '2020', '1.0', 'Gasolina', 'DEF2A34', 'Branco', NULL,              1, TRUE, '2026-01-13 10:00:00', NULL),
    (3, '10000000361', 'Gol',   'Volkswagen','2018', '2019', '1.6', 'Gasolina', 'GHI3B45', 'Preto',  NULL,              1, TRUE, '2026-01-13 10:00:00', NULL),
    (4, '10000000442', 'HB20',  'Hyundai',   '2022', '2023', '1.0', 'Álcool',   'JKL4C56', 'Vermelho', NULL,            1, TRUE, '2026-01-13 10:00:00', NULL);

INSERT INTO service (
    service_id, description, price, average_duration_minutes,
    user_modification_id, flag_active, insertion_date, modification_date
) VALUES
    (1, 'Troca de oleo',                 150.00,  45, 1, TRUE, '2026-01-08 08:00:00', NULL),
    (2, 'Troca de correia dentada',      350.00, 180, 1, TRUE, '2026-01-08 08:00:00', NULL),
    (3, 'Troca de pastilha de freio',    200.00,  90, 1, TRUE, '2026-01-08 08:00:00', NULL),
    (4, 'Troca de pneu',                  80.00,  30, 1, TRUE, '2026-01-08 08:00:00', NULL),
    (5, 'Alinhamento e balanceamento',   100.00,  40, 1, TRUE, '2026-01-08 08:00:00', NULL),
    (6, 'Revisao de arrefecimento',      180.00,  60, 1, TRUE, '2026-01-08 08:00:00', NULL);

INSERT INTO part (
    part_id, description, brand, manufacturer, unit_price, available_quantity,
    user_modification_id, flag_active, insertion_date, modification_date
) VALUES
    (1,  'Oleo motor 5W30 1L',           'Lubrax',  'Petrobras',     45.00, 40, 1, TRUE, '2026-01-08 08:00:00', NULL),
    (2,  'Filtro de oleo',               'Bosch',   'Bosch do Brasil', 50.00, 20, 1, TRUE, '2026-01-08 08:00:00', NULL),
    (3,  'Correia dentada',              'Gates',   'Gates',         180.00,  8, 1, TRUE, '2026-01-08 08:00:00', NULL),
    (4,  'Tensor da correia',            'Gates',   'Gates',         120.00,  8, 1, TRUE, '2026-01-08 08:00:00', NULL),
    (5,  'Pastilha de freio dianteira',  'Fras-le', 'Fras-le',       160.00, 12, 1, TRUE, '2026-01-08 08:00:00', NULL),
    (6,  'Pneu 185/60 R15',              'Pirelli', 'Pirelli',       320.00, 16, 1, TRUE, '2026-01-08 08:00:00', NULL),
    (7,  'Bico de pneu',                 'Schrader','Schrader',       15.00, 30, 1, TRUE, '2026-01-08 08:00:00', NULL),
    (8,  'Contrapeso de balanceamento',  'Tech',    'Tech',            8.00, 50, 1, TRUE, '2026-01-08 08:00:00', NULL),
    (9,  'Aditivo de radiador',          'Paraflu', 'Paraflu',        35.00, 15, 1, TRUE, '2026-01-08 08:00:00', NULL),
    (10, 'Tampa do reservatorio',        'Valeo',   'Valeo',          45.00, 10, 1, TRUE, '2026-01-08 08:00:00', NULL);

INSERT INTO stock_operation (operation_id, part_id, operation_type, quantity, order_part_id, operation_date) VALUES
    (1,  1,  'Entrada inicial', 40, NULL, '2026-01-08 08:30:00'),
    (2,  2,  'Entrada inicial', 20, NULL, '2026-01-08 08:30:00'),
    (3,  3,  'Entrada inicial',  8, NULL, '2026-01-08 08:30:00'),
    (4,  4,  'Entrada inicial',  8, NULL, '2026-01-08 08:30:00'),
    (5,  5,  'Entrada inicial', 12, NULL, '2026-01-08 08:30:00'),
    (6,  6,  'Entrada inicial', 16, NULL, '2026-01-08 08:30:00'),
    (7,  7,  'Entrada inicial', 30, NULL, '2026-01-08 08:30:00'),
    (8,  8,  'Entrada inicial', 50, NULL, '2026-01-08 08:30:00'),
    (9,  9,  'Entrada inicial', 15, NULL, '2026-01-08 08:30:00'),
    (10, 10, 'Entrada inicial', 10, NULL, '2026-01-08 08:30:00');

-- OS 1 Andrey/Civic oleo: 150 + (4*45 + 50) = 380, Jose, em execucao
-- OS 2 Andrey/Civic correia: 350 + (180 + 120) = 650, Jose, pecas em separacao
-- OS 3 Maria/Onix pastilha: 200 + 160 = 360, Pedro, aguardando aprovacao
-- OS 4 Joao/Gol pneu: 80 + (4*320 + 4*15) = 1420, Jose, pronto para iniciar
-- OS 5 Lucia/HB20 oleo+alinhamento: 250 + (4*45 + 50 + 4*8) = 512, sem mecanico
-- OS 6 Joao/Gol pastilha: 200 + 160 = 360, Pedro, rejeitada
-- OS 7 Andrey/Civic arrefecimento: 180 + (2*35 + 45) = 295, Jose, finalizada
INSERT INTO service_order (
    order_id, person_id, vehicle_id, mileage, reported_problem, diagnosis, mechanic_id,
    services_total, parts_total, total_amount, estimated_duration_days, notes, status,
    request_date, start_date, end_date, user_modification_id, flag_active, insertion_date, modification_date
) VALUES
    (1, '52998224725', 1, 85000,
        'Barulho no motor ao acelerar e oleo baixo',
        'Oleo vencido e filtro saturado. Trocar oleo e filtro.',
        '39053344705', 150.00, 230.00, 380.00, 1, NULL, 'Em execução',
        '2026-08-20 09:00:00', '2026-08-22 08:30:00', NULL, 1, TRUE, '2026-08-20 09:00:00', NULL),
    (2, '52998224725', 1, 85200,
        'Estalo na frente em baixa rotacao',
        'Correia dentada e tensor no fim da vida. Trocar o kit.',
        '39053344705', 350.00, 300.00, 650.00, 1, NULL, 'Peças em separação no estoque',
        '2026-08-21 10:00:00', NULL, NULL, 1, TRUE, '2026-08-21 10:00:00', NULL),
    (3, '10000000108', 2, 62000,
        'Chiado ao frear',
        'Pastilhas dianteiras no fim. Trocar o jogo.',
        '85351346893', 200.00, 160.00, 360.00, 1, NULL, 'Aguardando aprovação',
        '2026-08-22 11:00:00', NULL, NULL, 1, TRUE, '2026-08-22 11:00:00', NULL),
    (4, '10000000361', 3, 48000,
        'Pneus carecas e vibracao em reta',
        'Quatro pneus abaixo do limite. Trocar o jogo e os bicos.',
        '39053344705', 80.00, 1340.00, 1420.00, 1, NULL, 'Pronto para iniciar',
        '2026-08-23 14:00:00', NULL, NULL, 1, TRUE, '2026-08-23 14:00:00', NULL),
    (5, '10000000442', 4, 15000,
        'Revisao de oleo e direcao puxando',
        NULL,
        NULL, 250.00, 262.00, 512.00, 1, NULL, 'Aguardando mecânico',
        '2026-08-24 09:30:00', NULL, NULL, 1, TRUE, '2026-08-24 09:30:00', NULL),
    (6, '10000000361', 3, 48100,
        'Freio alto depois da troca de pneu',
        'Pastilhas ainda no limite. Cliente recusou a troca agora.',
        '85351346893', 200.00, 160.00, 360.00, 1, NULL, 'Rejeitada',
        '2026-08-25 08:00:00', NULL, NULL, 1, TRUE, '2026-08-25 08:00:00', NULL),
    (7, '52998224725', 1, 84000,
        'Motor esquenta no transito',
        'Aditivo fraco e tampa do reservatorio sem vedacao.',
        '39053344705', 180.00, 115.00, 295.00, 1, NULL, 'Finalizada',
        '2026-08-10 09:00:00', '2026-08-11 08:00:00', '2026-08-11 16:00:00', 1, TRUE, '2026-08-10 09:00:00', NULL);

INSERT INTO order_service (
    order_service_id, order_id, service_id, mechanic_id,
    user_modification_id, flag_active, insertion_date, modification_date
) VALUES
    (1, 1, 1, '39053344705', 1, TRUE, '2026-08-20 09:00:00', NULL),
    (2, 2, 2, '39053344705', 1, TRUE, '2026-08-21 10:00:00', NULL),
    (3, 3, 3, '85351346893', 1, TRUE, '2026-08-22 11:00:00', NULL),
    (4, 4, 4, '39053344705', 1, TRUE, '2026-08-23 14:00:00', NULL),
    (5, 5, 1, NULL,          1, TRUE, '2026-08-24 09:30:00', NULL),
    (6, 5, 5, NULL,          1, TRUE, '2026-08-24 09:30:00', NULL),
    (7, 6, 3, '85351346893', 1, TRUE, '2026-08-25 08:00:00', NULL),
    (8, 7, 6, '39053344705', 1, TRUE, '2026-08-10 09:00:00', NULL);

INSERT INTO order_part (
    order_part_id, order_id, part_id, quantity, total_amount,
    user_modification_id, flag_active, insertion_date, modification_date
) VALUES
    (1,  1, 1,  4, 180.00, 1, TRUE, '2026-08-20 09:00:00', NULL),
    (2,  1, 2,  1,  50.00, 1, TRUE, '2026-08-20 09:00:00', NULL),
    (3,  2, 3,  1, 180.00, 1, TRUE, '2026-08-21 10:00:00', NULL),
    (4,  2, 4,  1, 120.00, 1, TRUE, '2026-08-21 10:00:00', NULL),
    (5,  3, 5,  1, 160.00, 1, TRUE, '2026-08-22 11:00:00', NULL),
    (6,  4, 6,  4, 1280.00, 1, TRUE, '2026-08-23 14:00:00', NULL),
    (7,  4, 7,  4,  60.00, 1, TRUE, '2026-08-23 14:00:00', NULL),
    (8,  5, 1,  4, 180.00, 1, TRUE, '2026-08-24 09:30:00', NULL),
    (9,  5, 2,  1,  50.00, 1, TRUE, '2026-08-24 09:30:00', NULL),
    (10, 5, 8,  4,  32.00, 1, TRUE, '2026-08-24 09:30:00', NULL),
    (11, 6, 5,  1, 160.00, 1, TRUE, '2026-08-25 08:00:00', NULL),
    (12, 7, 9,  2,  70.00, 1, TRUE, '2026-08-10 09:00:00', NULL),
    (13, 7, 10, 1,  45.00, 1, TRUE, '2026-08-10 09:00:00', NULL);

COMMIT;
