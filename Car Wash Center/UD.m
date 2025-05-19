function rn = UD(n)
    randNumbers = zeros(1, n);

%declare the min and max    
    a = 1; 
    b = 99; 
    
    % Generate the random variates
    for i = 1:n
        x = rand(); 
        randNumbers(i) = a + (b - a) * x; 
    end
    
    rn = randNumbers;
end
