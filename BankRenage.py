"""
Bank renege example # renege: customers who leave without service

Covers:

- Resources: Resource
- Condition events

Scenario:
  A counter with a random service time and customers who renege. Based on the
  program bank08.py from TheBank tutorial of SimPy 2. (KGM)

"""
import random

import simpy


RANDOM_SEED = 42
NEW_CUSTOMERS = 5  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 3  # Max. customer patience

""""   env.process tells Source how many NUMBER of NEW_CUSTOMERS to create, and their INTER arriVAL_CUSTOMERS time """"
""""   Source creates/calls Customers""""
def source(env, number, interval, counter):
    """Source generates customers randomly"""
    for i in range(number): # i will be used as serial# to keep track how many customers created
        # Customer(env, name:=Customer+Serial#, # of customer service counters:=1, Parameter to decide Cycletime_in_bank service counter)
        c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0) # call to funtion which creates a customer
        env.process(c) # Put the customer into environment
        t = random.expovariate(1.0 / interval) # Get random & inverse of interval(INTERVAL_CUSTOMERS) to ..
        yield env.timeout(t) # wait for next arrival


def customer(env, name, counter, time_in_bank): # function to create a customer
    """Customer arrives, is served and leaves."""
    arrive = env.now # note down current time
    print('%7.4f %s: Here I am' % (arrive, name)) # PRINT " TIME Customer##: Here I am"

    with counter.request() as req: # ??? the actual waiting time needed to get counter
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE) # Uniform distribution, how long customers are willing to wait
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience) # OR condition to trigger yeild until first event (min of two)

        wait = env.now - arrive # Calculate waiting time in queue for customer before executing first available event

        if req in results: # if this is first event if customer is lucky
            # We got to the counter
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait)) #PRINT "TIME Customer##: Waited  WaitingTime"

            tib = random.expovariate(1.0 / time_in_bank)
            yield env.timeout(tib)
            print('%7.4f %s: Finished' % (env.now, name)) # PRINT "TIME Customer##: Finished"

        else: # if patiance is ended befre getting the counter
            # We reneged
            print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait)) # print "TIME Customer#: RENEGED after WaitingTime"


# Setup and start the simulation
print('Bank renege') # PRINT Title of the Model
random.seed(RANDOM_SEED) # Set random seed
env = simpy.Environment() # something required for every simulation

# Start processes and run
counter = simpy.Resource(env, capacity=1) # Create 1 customer service counter
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()
