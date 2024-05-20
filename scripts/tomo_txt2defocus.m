run /opt/dynamo/dynamo_activate.m;

cd('RR-LB-36-10');

% 定义文件夹的前缀和递增序号范围
prefix = '20240503_RR-LB-36-10_';
start_index = 1;
end_index = 36;
ctfraw = 'diagnostic_output.txt';

for i = start_index:end_index
    folder_name = strcat(prefix, num2str(i, '%04d'));
    tltfile = strcat(folder_name, '.tlt');
    defocusfile = strcat(folder_name, '.defocus');
    cd(folder_name); % 进入文件夹

    if exist(ctfraw, 'file') == 0
        disp(['error: no ctffind .txt result, skipped ', folder_name]);
        cd('..');
        continue;
    end
    if exist(tltfile, 'file') == 0
        disp(['error: no imod .tlt result, skipped ', folder_name]);
        cd('..');
        continue;
    end
    if exist(defocusfile, 'file') == 2
        disp(['error: there is a .defocus file, skipped ', folder_name]);
        cd('..');
        continue;
    end
    
    % 执行命令
    dpcomp.ctffind.forImod(ctfraw, tltfile, defocusfile);
    cd('..'); % 退出文件夹
end

cd('..');
disp('done');

