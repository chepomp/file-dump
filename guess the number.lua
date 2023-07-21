local number = math.random(1, 10)

print "I am thinking of a number between 1 and 10! You have 5 attempts to guess my number! \n"

repeat
    local guess = io.read();
    local guess = tonumber(guess)

    if guess > number then
        print "Your guess is too high!"
    elseif 
        guess < number then
            print "Your guess is too low!"
    end

until
    guess == number
    print "You guessed my number!"