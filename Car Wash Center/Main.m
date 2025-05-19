function Main(x)
    disp('Choose the type of generator:');
    fprintf('1 = linear congruential generators (LCG)\n'); % Added \n for newline
    disp('2 = Random Variate Generator for Uniform Distribution (UD)');
    getGenerator = input('Enter type of generator: ');
    disp(' ');
    
    detect = true;
    while detect
        if getGenerator == 1
            Generator = 1; % LCG function
            fprintf('Your generator type : LCG\n\n');
            detect = false;
        elseif getGenerator == 2
            Generator = 2; % RUG function
            fprintf('Your generator type : UD\n\n');
            detect = false;
        else
            disp('Invalid input please try again');
            getGenerator = input('Enter type of generator: ');

        end
    end

    %initialization Service time and Probability for wash bar 1 2 3 
    setService1 = [6,7,8,9,10];
    setService2 = [4,5,6,7,8];
    setService3 = [3,4,5,6,7];    
    setProb1 = randProb(5);
    setProb2 = randProb(5);
    setProb3 = randProb(5);    
    bayService = {setService1,setService2,setService3};
    bayProb = {setProb1,setProb2,setProb3};    
    bayTable(bayService,bayProb); 
    %initialization interarrival time and Probaboility
    setInter = [1,2,3,4,5];
    setInterProb = randProb(5);    
    interTable(setInter,setInterProb);
    InterProbCumulative = cumsum(setInterProb) / sum(setInterProb);    
    %initialization Service Type
    serviceTypes = [1,2];
    serviceTypeProbs = [50,50];    
    typeTable(serviceTypes,serviceTypeProbs);
    numCustomers = input('Enter Number of customers: ');            
    fprintf('Total customers: %d\n', numCustomers); 
    disp(' ');    
    % Call Simulation function
    Simulation(Generator,numCustomers, setInter, InterProbCumulative, serviceTypes, serviceTypeProbs,bayService,bayProb);
end
