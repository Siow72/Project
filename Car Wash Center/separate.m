function separate(numCustomers, Inter, InterProbCumulative, bayService, bayProb, getGenerator, arrtime, type,interArr)
    
    % Initialize arrays to store results
    n = zeros(1, numCustomers);                
    rn = rand(1, numCustomers);                
    setBay = zeros(1, numCustomers);           
    serviceTime = zeros(1, numCustomers);     
    timeServiceBegin = zeros(1, numCustomers); 
    timeServiceEnd = zeros(1, numCustomers);   
    waitingTime = zeros(1, numCustomers);     
    timeSpendsInSystem = zeros(1, numCustomers); 
    interArrivalTimes = rand(1, numCustomers);     
    
    if getGenerator == 1 
        rnServiceTimes = LCG(numCustomers); 
    else 
        rnServiceTimes = UD(numCustomers); 
    end 
    
    timeServiceEndBay1 = 0; 
    timeServiceEndBay2 = 0; 
    timeServiceEndBay3 = 0; 
    count = 0;

    % Assign customers to bays based on their arrival times
    for i = 1:numCustomers
        n(i) = i;
        rn(i) = round(rnServiceTimes(i));
        setInter(i) = interArr(i);
        % For the first customer
        if i ==1 
            waitingTime(i) = 0;
            timeServiceBegin(i) = arrtime(i);
            setBay(i) = i;
            % Calculate service time based on bay assignment
            serviceTimeRange = bayService{setBay(i)};
            prob = bayProb{setBay(i)};
            
            cumulativeProb = cumsum(prob / sum(prob)) * 100;
            serviceTimeIndex = find(rn(i) <= cumulativeProb, 1, 'first');
            serviceTime(i) = serviceTimeRange(serviceTimeIndex);
            
            % Calculate other times
            timeServiceEnd(i) = timeServiceBegin(i) + serviceTime(i);
            timeSpendsInSystem(i) = serviceTime(i) + waitingTime(i);
            
            messages(i,arrtime(i),waitingTime(i),setBay(i),timeServiceEnd(i),timeServiceBegin(i),serviceTime(i));
            
            % Update end time for the assigned bay
            switch setBay(i)
                case 1
                    timeServiceEndBay1 = timeServiceEnd(i);
                case 2
                    timeServiceEndBay2 = timeServiceEnd(i);
                case 3
                    timeServiceEndBay3 = timeServiceEnd(i);
            end
           
        else
            arrivalTime = arrtime(i); 
            suitableBayFound = false; 
            firstSuitableBay = 0;
            for j = 1:3 
                if arrivalTime >= bayEnd(j) 
                    firstSuitableBay = j; 
                    suitableBayFound = true;
                    break;
                end 
            end
            if suitableBayFound
                setBay(i) = firstSuitableBay;
                timeServiceBegin(i) = arrivalTime;
            else
                % fall back to assigning based on the minimum end time
                [minEndTime, bayIndex] = min(bayEnd);
                setBay(i) = bayIndex;
                timeServiceBegin(i) = minEndTime;
            end

            % Calculate service time based on bay assignment
            serviceTimeRange = bayService{setBay(i)};
            prob = bayProb{setBay(i)};
            
            cumulativeProb = cumsum(prob / sum(prob)) * 100;
            serviceTimeIndex = find(rn(i) <= cumulativeProb, 1, 'first');
            serviceTime(i) = serviceTimeRange(serviceTimeIndex);
            
            % Calculate other times
            timeServiceEnd(i) = timeServiceBegin(i) + serviceTime(i);
            waitingTime(i) = timeServiceBegin(i) - arrtime(i);
            timeSpendsInSystem(i) = serviceTime(i) + waitingTime(i);
            if waitingTime(i) >0
                count = count+1;
            end
            
            % Update end time for the assigned bay
            switch setBay(i)
                case 1
                    timeServiceEndBay1 = timeServiceEnd(i);
                case 2
                    timeServiceEndBay2 = timeServiceEnd(i);
                case 3
                    timeServiceEndBay3 = timeServiceEnd(i);
            end
            messages(i,arrtime(i),waitingTime(i),setBay(i),timeServiceEnd(i),timeServiceBegin(i),serviceTime(i));
                        
        end
        bayEnd = [timeServiceEndBay1, timeServiceEndBay2, timeServiceEndBay3];
    end
    % Display results for each bay
    for bay = 1:3
        fprintf('\n Wash Bay %d:\n', bay);
        fprintf('  n  | RN for service time | Service Time | Time Service Begin | Time Service End | Waiting Time | Time Spent in System \n');
        fprintf('-----------------------------------------------------------------------------------------------------------------------\n');
        for i = 1:numCustomers
            if setBay(i) == bay
                fprintf(' %3d | %19d | %12d | %18d | %16d | %12d | %18d \n', ...
                    n(i), rn(i), serviceTime(i), timeServiceBegin(i), timeServiceEnd(i), waitingTime(i), timeSpendsInSystem(i));
            end
        end
    end
    
    %calculate all the evaluate
    cus1 = sum(setBay==1);
    cus2 = sum(setBay==2);
    cus3 = sum(setBay==3);
    cus = numCustomers;
    
    avgWait1 = sum(waitingTime(setBay==1))/cus1;
    avgWait2 = sum(waitingTime(setBay==2))/cus2;
    avgWait3 = sum(waitingTime(setBay==3))/cus3;
    avgTWait = sum(waitingTime)/cus;
    
    avgProb1 = sum(waitingTime(setBay == 1) > 0) / cus1;
    avgProb2 = sum(waitingTime(setBay == 2) > 0) / cus2;
    avgProb3 = sum(waitingTime(setBay == 3) > 0) / cus3;
    avgTProb = count / cus;
    
    avgTimeSpent1 = sum(timeSpendsInSystem(setBay ==1))/cus1;
    avgTimeSpent2 = sum(timeSpendsInSystem(setBay==2))/cus2;
    avgTimeSpent3 = sum(timeSpendsInSystem(setBay==3))/cus3;
    avgTTime = sum(timeSpendsInSystem)/cus;

    avgServiceTimeBay1 = mean(serviceTime(setBay == 1));
    avgServiceTimeBay2 = mean(serviceTime(setBay == 2));
    avgServiceTimeBay3 = mean(serviceTime(setBay == 3));
    avgTService = sum(serviceTime)/cus;
    
    avgInter = sum(setInter)/(cus-1);

    avgservice = {avgServiceTimeBay1,avgServiceTimeBay2,avgServiceTimeBay3};
    avgWait = {avgWait1,avgWait2,avgWait3};
    avgTimeSpent= {avgTimeSpent1,avgTimeSpent2,avgTimeSpent3};
    avgProb = {avgProb1,avgProb2,avgProb3};
    
    display(avgservice,avgWait,avgTimeSpent,avgProb,);
    displaytotal(avgTWait,avgTTime,avgTService,avgInter,avgTProb);
   
end

%function to print out the general message
function messages(i, arrtime, waitTime, setBay, timeServiceEnd, timeServiceBegin,servicetime)
    fprintf('\n --General Information--\n');
    msg = sprintf(['Arrival of customer %d at minute %d.\n', ...
                   'Queue at Wash Bay %d.\n', ...
                   'Customer waited %d minutes.\n', ...
                   'Customer %d started service at minute %d and departed at minute %d.\n', ...
                   'Service time for customer %d is %d.\n',...
                   'Service for next customer at Wash Bay %d at minute %d.\n'], ...
                   i, arrtime, setBay, waitTime, i, timeServiceBegin, timeServiceEnd,i,servicetime, setBay, timeServiceEnd);
    disp(msg);
end

%function for display evaluate message for each wash bay
function display(avgservice, avgWait, avgTimeSpent, avgProb)
    for bay = 1:3
        
        fprintf('\nEvaluate for Wash Bay %d:\n', bay);
        fprintf('-------------------------\n');

        fprintf('Average Service Time: %.2f\n', avgservice{bay});

        fprintf('Average Waiting Time: %.2f\n', avgWait{bay});

        fprintf('Average Time Spent in System: %.2f\n', avgTimeSpent{bay});

        fprintf('Probability of Waiting: %.2f\n', avgProb{bay});


        fprintf('\n');
    end
end

%function for display evaluate message for simulation
function displaytotal(avgTWait,avgTTime,avgTService,avgInter,avgTProb)
        
        fprintf('\nEvaluate for simulation :\n');
        fprintf('-------------------------\n');

        fprintf('Average Service Time: %.2f\n', avgTService);

        fprintf('Average Waiting Time: %.2f\n', avgTWait);

        fprintf('Average Time Spent in System: %.2f\n', avgTTime);

        fprintf('Average of Inter-arrival time: %.2f\n', avgInter);
                
        fprintf('Probability of Waiting: %.2f\n', avgTProb);

        fprintf('\n');
    
end