function interTable(Inter, InterProb)
    % Initialize cumulative probability
    fprintf('Inter-arrival Time Table : \n');
    disp('  Inter-arrival Time | Probability |  CDF  |  Range  ');
    fprintf('%s\n', repmat('-', 1, 55));  % print a line of dashes   
    
    cdf = 0;
    
    for i = 1:length(Inter)
        prob = InterProb(i) / 100;
        cdf = prob + cdf;
        rangeStart = sum(InterProb(1:i-1)) + 1; 
        rangeEnd = rangeStart + InterProb(i) - 1;  % Calculate range end

        % Display table row
        fprintf('|       %d            |    %.2f     |  %.2f | %2d - %-3d \n', ...
            Inter(i), prob, cdf, rangeStart, rangeEnd);
    end
    disp(' ');

end
