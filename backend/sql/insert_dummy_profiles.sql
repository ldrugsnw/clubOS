-- Insert dummy profiles data
INSERT INTO profiles (id, name, department, student_id, gender, phone_number, slack_user_id)
VALUES
    (gen_random_uuid(), '김영희', '컴퓨터공학과', '20240001', '여성', '010-1234-5678', 'SLACK001'),
    (gen_random_uuid(), '이철수', '소프트웨어학과', '20240002', '남성', '010-2345-6789', 'SLACK002'),
    (gen_random_uuid(), '박지민', '정보통신공학과', '20240003', '여성', '010-3456-7890', 'SLACK003'),
    (gen_random_uuid(), '최민준', '컴퓨터공학과', '20240004', '남성', '010-4567-8901', 'SLACK004'),
    (gen_random_uuid(), '정다은', '인공지능학과', '20240005', '여성', '010-5678-9012', 'SLACK005'),
    (gen_random_uuid(), '강현우', '소프트웨어학과', '20240006', '남성', '010-6789-0123', 'SLACK006'),
    (gen_random_uuid(), '송지원', '컴퓨터공학과', '20240007', '여성', '010-7890-1234', 'SLACK007'),
    (gen_random_uuid(), '임준호', '정보통신공학과', '20240008', '남성', '010-8901-2345', 'SLACK008'),
    (gen_random_uuid(), '한소희', '인공지능학과', '20240009', '여성', '010-9012-3456', 'SLACK009'),
    (gen_random_uuid(), '오민석', '소프트웨어학과', '20240010', '남성', '010-0123-4567', 'SLACK010'); 