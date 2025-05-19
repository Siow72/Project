function typeTable(Type, typeProb)
    name = cell(1, length(Type)); % Use cell array to store strings
    fprintf('Type Table : \n'); % Updated header
    fprintf('  Type          | Probability |  CDF  | Range\n'); 
    fprintf('%s\n', repmat('-', 1, 46)); % print a line of dashes
    cdf = 0;
    
    for i = 1:length(Type)
        if Type(i) == 1
            name{i} = ' Normal Wash';
        elseif Type(i) == 2
            name{i} = ' Wash + Polish';
        end
        
        % Get probability
        prob = typeProb(i) / 100;
        cdf = prob + cdf;
        rangeStart = sum(typeProb(1:i-1)) + 1; 
        rangeEnd = rangeStart + typeProb(i) - 1;
        % Display table row
        fprintf('%-15s |    %.2f     |  %.2f | %2d - %3d\n', name{i}, prob, cdf, rangeStart, rangeEnd);
    end
    disp(' ');
    disp('Assume 1 = Normal Wash | 2 = Wash + Polish');
    disp(' ');
end
