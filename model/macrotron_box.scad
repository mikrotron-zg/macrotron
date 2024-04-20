/*
 * This file is part of macrotron project
 * (https://github.com/mikrotron-zg/macrotron)
 * developed by Mikrotron d.o.o. (http://mikrotron.hr).
 * It contains box 3D model used for this project.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version. See the LICENSE file at the 
 * top-level directory of this distribution for details 
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

/****************************************************************************
 **************************** Global Variables ******************************
 ****************************************************************************/

/* List of shorthands in variable names:
 * mh -> short for 'mount hole'
 * dia -> diameter
 * pos -> position
 */

// NeoKey board dimensions
neokey_pcb_length = 76.2;
neokey_pcb_width = 21.6;
neokey_pcb_height = 1.6;
neokey_corner_radius = 2.5;
neokey_mh_dia = 2.54;
neokey_mh_offset = 19.05;
neokey_mh_pos = [ [neokey_mh_offset, neokey_mh_dia], 
                  [neokey_pcb_length - neokey_mh_offset, neokey_mh_dia],
                  [neokey_mh_offset, neokey_pcb_width - neokey_mh_dia],
                  [neokey_pcb_length - neokey_mh_offset, neokey_pcb_width - neokey_mh_dia] ];

// Utility variables
$fn = 150; // Makes rounded object smoother
ex = 0.001; // Extra dimension to remove wall ambiguity in preview mode

/****************************************************************************
 ****************************** Main Modules ********************************
 ****************************************************************************/

// Start point
macrotron_box();

module macrotron_box() {
    neokey_pcb();
}

/****************************************************************************
 ***************** Additional Modules and Functions *************************
 ****************************************************************************/

// Draws a rounded rectangle
module rounded_rect(x, y, z, radius = 1) {
    translate([radius,radius,0]) //move origin to outer limits
	linear_extrude(height=z)
		minkowski() {
			square([x-2*radius,y-2*radius]); //keep outer dimensions given by x and y
			circle(r = radius);
		}
}

// Draws NeoKey PCB mockup
module neokey_pcb() {
    difference() {
        rounded_rect(neokey_pcb_length, neokey_pcb_width, neokey_pcb_height, neokey_corner_radius);
        for (i = [0:3]) translate(zex()) {
            translate(neokey_mh_pos[i]) cylinder(d = neokey_mh_dia, h = neokey_pcb_height + 2*ex);
        }
    }
}

// Move to -ex on z axis
function zex() = [0, 0, -ex];