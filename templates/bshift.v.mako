<%! from vmako import connect,ev,instance,log2 %>

module bshift_${w} (
  input clk,
  input [${ev(w-1)}:0] in,
  input [${ev(log2(w)-1)}:0] cnt,
  output reg [${ev(w-1)}:0] out
);

% for i in range(1, w):
wire [${ev(w-1)}:0] out_${i} = {in[${ev(w-i-1)}:0], in[${ev(w-1)}:${ev(w-i)}]};
% endfor

always @(*)
  case (cnt)
% for i in range(1, w):
    ${i}: out = out_${i};
% endfor
    default: out = in;
  endcase

${instance('$HOME/raid/vmako/templates/dff.v.mako',
           "u_dff",
           w=w
          )}

endmodule //bshift_${w}