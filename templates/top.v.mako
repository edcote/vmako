<%! from vmako import connect, ev,instance,log2 %>

module top;

bit clk = 0;

## instantiate 2x 'w'-bit wide barrel shifters

% for i in range(0, 2):
## define local variable inst
<% inst = 'u{}_bshf_{}'.format(i,w) %>
${instance('$HOME/raid/vmako/templates/bshift.v.mako',
           inst,
           w=w
          )}
## connect dest <- src
${connect((inst, 'clk'), ('', 'clk'))}
% endfor

## example connect between modules
${connect(('u1_bshf_'+str(w), 'in'), ('u0_bshf_'+str(w), 'out'))}

endmodule //top
