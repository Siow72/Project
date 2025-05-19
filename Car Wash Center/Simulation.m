function Simulation(generator,numCustomers, interArrivalTimes, interArrivalProbs, serviceTypes, serviceTypeProbs,bayService,bayProb)
    % Generate random numbers using LCG for inter-arrival times
    if generator ==1
        disp('using LCG');
        rnInterArrivals = round(LCG(numCustomers));
        rnServiceTypes = round(LCG(numCustomers));  

    elseif generator == 2
        rnInterArrivals = round(UD(numCustomers));
        rnServiceTypes = round(LCG(numCustomers));

    end

    % Generate random numbers for service type using UD (Uniform Distribution)
    
    % Initialize arrays to store results
    arrivalTimes = zeros(1, numCustomers);
    serviceTypeList = zeros(1, numCustomers);
    interArr = zeros(1,numCustomers);
    
    fprintf(' n  | RN for Inter-arrival time | Inter-arrival time | Arrival time | Service type \n');
    fprintf('-----------------------------------------------------------------------------------\n');
    
    % Customer data generation loop
    for n = 1:numCustomers
        % Determine inter-arrival time display and value
        if n == 1
            interArrivalTimeDisplay = '0'; % Display hyphen for the first inter-arrival time
            interArrivalTime = 0; % Initial inter-arrival time is 0
                                
        else
            found = false;
            for i = 1:length(interArrivalTimes)
                if rnInterArrivals(n) < interArrivalProbs(i) * 100 
                    interArrivalTimeDisplay = num2str(interArrivalTimes(i));
                    interArrivalTime = interArrivalTimes(i);
  
                    found = true;
                    break;
                end
            end
            interArr(n) = interArrivalTime;
            % If no valid inter-arrival time found
            if ~found
                interArrivalTimeDisplay = 'Error';
                interArrivalTime = NaN; 
            end
        end
        
        % Calculate arrival time
        if n == 1
            arrivalTimes(n) = 0; % First arrival time is set to 1
        else
            arrivalTimes(n) = round(arrivalTimes(n-1) + interArrivalTime); % Calculate and round arrival time
        end
        
        % Determine service type based on random number and probabilities
        cumulativeProb = 0;
        for i = 1:length(serviceTypes)
            cumulativeProb = cumulativeProb + serviceTypeProbs(i);
            if rnServiceTypes(n) <= cumulativeProb
                serviceTypeList(n) = serviceTypes(i);
                break;
            end
        end
        
        % Display customer data
        fprintf(' %2d | %25s | %17s | %12d | %12d \n', ...
            n, ifelse(n == 1, '0', num2str(rnInterArrivals(n))), interArrivalTimeDisplay, arrivalTimes(n), serviceTypeList(n));
    end
    % Call Separate function
    separate(numCustomers, interArrivalTimes, interArrivalProbs,bayService, bayProb,generator,arrivalTimes,serviceTypeList,interArr);
end

function res = ifelse(cond, true_val, false_val)
    
    % Helper function to replicate the ifelse function from other languages
    if cond
        res = true_val;
    else
        res = false_val;
    end
end
