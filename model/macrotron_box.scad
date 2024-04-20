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

// Adafruit QT Py dimensions
qtpy_pcb_length = 20.8;
qtpy_pcb_width = 17.8;
qtpy_pcb_height = 1.6;
qtpy_corner_radius = 2.5;
qtpy_usbc_clearance = 1.6;

// NeoKey board dimensions
neokey_pcb_length = 76.2;
neokey_pcb_width = 21.6;
neokey_pcb_height = 1.6;
neokey_pcb_clearance = 2.5;
neokey_corner_radius = 2.5;
neokey_mh_dia = 2.5;
neokey_mh_offset = 19.05;
neokey_mh_pos = [ [neokey_mh_offset, neokey_mh_dia], 
                  [neokey_pcb_length - neokey_mh_offset, neokey_mh_dia],
                  [neokey_mh_offset, neokey_pcb_width - neokey_mh_dia],
                  [neokey_pcb_length - neokey_mh_offset, neokey_pcb_width - neokey_mh_dia] ];

// Box dimensions
box_wall = 3;
box_wall_overlap = 3;
box_component_spacing = 10;
box_channel_width = neokey_pcb_width - 2*neokey_pcb_clearance;
box_channel_height = 5;
box_length = qtpy_pcb_length + neokey_pcb_length + 2*box_wall + 2*box_component_spacing;
box_width = neokey_pcb_width + 2*box_wall;
box_bottom_height = box_wall + box_channel_height + neokey_pcb_height + box_wall_overlap;
box_inner_radius = 2.5;
box_corner_radius = box_wall + box_inner_radius;
// Utility variables
$fn = 150; // Makes rounded object smoother
ex = 0.001; // Extra dimension to remove wall ambiguity in preview mode

/****************************************************************************
 ****************************** Main Modules ********************************
 ****************************************************************************/

// Start point
macrotron_box();

module macrotron_box() {
    box_bottom();
    //usbc_connector(qtpy_usbc_clearance);
}

module box_bottom() {
    difference() {
        // Main body
        rounded_rect(box_length, box_width, box_bottom_height, box_corner_radius);
        // Overlap
        translate([box_wall/2, box_wall/2, box_bottom_height - box_wall_overlap])
            rounded_rect(box_length - box_wall, box_width - box_wall, 
                         box_wall_overlap + ex, box_inner_radius);
        // Channel
        translate([box_wall, box_width/2 - box_channel_width/2, box_wall])
            cube([box_length - 2*box_wall, box_channel_width, box_channel_height + neokey_pcb_height + ex]);
        // QT Py slot
        translate([box_wall, box_width/2 - qtpy_pcb_width/2, 
                   box_bottom_height - box_wall_overlap - qtpy_pcb_height + ex]) qtpy_pcb();
        // NeoKey slot
        translate([box_wall + qtpy_pcb_length + box_component_spacing, box_width/2 - neokey_pcb_width/2, 
                   box_bottom_height - box_wall_overlap - neokey_pcb_height + ex]) neokey_pcb();
        // USB-C cutout
        translate([-ex, box_width/2, box_bottom_height - box_wall_overlap])
            rotate(-90) usbc_connector(qtpy_usbc_clearance);
    }
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
module neokey_pcb(mount_holes = true) {
    difference() {
        rounded_rect(neokey_pcb_length, neokey_pcb_width, neokey_pcb_height, neokey_corner_radius);
        if (mount_holes) {
            for (i = [0:3]) translate(zex()) {
                translate(neokey_mh_pos[i]) cylinder(d = neokey_mh_dia, h = neokey_pcb_height + 2*ex);
            }
        }
    }
}

// Draws QT Py PCB mockup
module qtpy_pcb() {
    rounded_rect(qtpy_pcb_length, qtpy_pcb_width, qtpy_pcb_height, qtpy_corner_radius);
}

// Draws USB-C connector mockup
module usbc_connector(clearance = 0) {
    width = 8.34;
    length = 10.5;
    height = 2.65;
    translate([-width/2 - clearance, 10.5, - clearance]) rotate([90, 0, 0]) 
        rounded_rect(width + 2*clearance, height + 2*clearance, length, 1.2 + clearance);
}

// Move to -ex on z axis
function zex() = [0, 0, -ex];