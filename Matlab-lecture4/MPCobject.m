
clear all;clc
m=23.8;
ma=2;
Rs=1.44;
sys=ss((1+(Rs/(m+ma))),1/(m+ma),1,0,1);   %Defining the the state space form in discrete time
Vref=0.1; % Reference signal
%% disturbances
Vc=0%-0.05; % current speed
tau_wave_amp=0%0.05;% amplitude of the wave forces
tau_wave_freq=0%1;% frequency of the wave forces
%% Operational constraints
MV = struct('Min',0,'Max',5);    %Bounds for tau
MO = struct('Min',0,'Max',.2);    %Bounds for V

%% --------------------------MPC Controller------------------------------------------- 
tend=100;
horizon=2;              %Prediction horizon

MPCobj=mpc(sys,1,horizon,horizon,[],MV,MO); % Defining the MPC controller

alpha=100;
beta=0;

MPCobj.Weights.OutputVariables = alpha;          %Weights for the output measured variable (y)
MPCobj.Weights.ManipulatedVariables = beta;      %Weights for the actions (u)

%% --------------------------Controller------------------------------------------- 
MPCobj2=mpc(sys,1,tend,tend,[],MV,MO);

alpha2=alpha;
beta2=beta;

MPCobj2.Weights.OutputVariables = alpha2;
MPCobj2.Weights.ManipulatedVariables = beta2;
