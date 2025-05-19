function y = randProb(n)
    y = zeros(1, n);
    totalSum = 0; 
    
    for i = 1:n
        if i < n 
            y(i) = round(10 + rand * 18); % Generate value (10-28)
            totalSum = totalSum + y(i);
            
            while totalSum >= 90 % 
                totalSum = totalSum - y(i);
                y(i) = 0;
                y(i) = round(1 + rand * 25);
                totalSum = totalSum + y(i);
            end
        else
            y(n) = 100 - totalSum;
        end
    end               
end
