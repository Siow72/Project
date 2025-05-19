function randomNumbers = LCG(numCustomers)

    m = 6; 
    a = 9; 
    c = 5; 
    seed = 10; 

    
    randomNumbers = zeros(1, numCustomers); 
    x = rand *seed; 
   
    % Generate random numbers 
    for i = 1:numCustomers 
        x = mod(a * x + c, m); 
        randomNumbers(i) = (x / m)*100;
        if randomNumbers(i) > 99;
            randomNumbers(i) =99;
        elseif randomNumbers(i) < 1
            randomNumbers(i) =1;     
    end 
end
