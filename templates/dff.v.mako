<%! from vmako import ev,log2 %>

module dff_${w} (
  input clk,
  input [${ev(w-1)}:0] d,
  output reg [${ev(w-1)}:0] q
);

always @(posedge clk)
  q <= d;

endmodule