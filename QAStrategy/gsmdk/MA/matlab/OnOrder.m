function [  ] = OnOrder( order )
msg = sprintf('order status changed to %d, filled volume = %d', order(1, 'status'), order(1, 'filled_volume'))
disp(msg);

end