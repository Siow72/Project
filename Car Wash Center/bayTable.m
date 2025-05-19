function y = showBay(bayService, bayProb)
    for counter = 1:numel(bayService)
        
        disp(['Wash Bay : ', num2str(counter),]);
        disp('  Service Time | Probability |  CDF  |  Range  ');
        fprintf('%s\n', repmat('-', 1, 55));  % print a line of dashes
        cdf = 0;  % Cumulative distribution function values
        
        for i = 1:numel(bayService{counter})
            prob = bayProb{counter}(i) / 100;  % Probability for the current service time
            cdf = prob + cdf;
            rangeStart = sum(bayProb{counter}(1:i-1)) + 1; 
            rangeEnd = rangeStart + bayProb{counter}(i) - 1;
            fprintf('       %2d      |    %.2f     |  %.2f | %2d - %-3d\n', ...
                bayService{counter}(i), prob, cdf, rangeStart, rangeEnd);
        end
        disp(' ');
    end
end
