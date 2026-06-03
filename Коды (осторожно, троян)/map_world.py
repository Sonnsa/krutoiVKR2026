<?xml version="1.0" ?>
<sdf version="1.6">

  <world name="map_world">

    <include>
      <uri>model://sun</uri>
    </include>

    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- TOP WALL -->

    <model name="top_wall">
      <static>true</static>
      <pose>0 2 0.5 0 0 0</pose>

      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>4.2 0.12 1</size>
            </box>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <box>
              <size>4.2 0.12 1</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>

    <!-- LEFT WALL -->

    <model name="left_wall">
      <static>true</static>
      <pose>-2 0 0.5 0 0 0</pose>

      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.12 4.2 1</size>
            </box>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <box>
              <size>0.12 4.2 1</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>

    <!-- RIGHT WALL -->

    <model name="right_wall">
      <static>true</static>
      <pose>2 0 0.5 0 0 0</pose>

      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.12 4.2 1</size>
            </box>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <box>
              <size>0.12 4.2 1</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>

    <!-- BOTTOM WALL LEFT -->

    <model name="bottom_wall_left">
      <static>true</static>
      <pose>-1.25 -2 0.5 0 0 0</pose>

      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>1.6 0.12 1</size>
            </box>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <box>
              <size>1.6 0.12 1</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>

    <!-- BOTTOM WALL RIGHT -->

    <model name="bottom_wall_right">
      <static>true</static>
      <pose>1.25 -2 0.5 0 0 0</pose>

      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>1.6 0.12 1</size>
            </box>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <box>
              <size>1.6 0.12 1</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>

    <!-- CORRIDOR LEFT WALL -->

    <model name="corridor_left_wall">
      <static>true</static>
      <pose>-0.45 -2.75 0.5 0 0 0</pose>

      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.12 1.6 1</size>
            </box>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <box>
              <size>0.12 1.6 1</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>

    <!-- CORRIDOR RIGHT WALL -->

    <model name="corridor_right_wall">
      <static>true</static>
      <pose>0.45 -2.75 0.5 0 0 0</pose>

      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.12 1.6 1</size>
            </box>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <box>
              <size>0.12 1.6 1</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>

    <!-- CORRIDOR BOTTOM WALL -->

    <model name="corridor_bottom_wall">
      <static>true</static>
      <pose>0 -3.55 0.5 0 0 0</pose>
<link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>1.0 0.12 1</size>
            </box>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <box>
              <size>1.0 0.12 1</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>

    <!-- ROUND OBSTACLE -->

    <model name="round_obstacle">
      <static>true</static>
      <pose>-1.2 0.8 0.35 0 0 0</pose>

      <link name="link">
        <collision name="collision">
          <geometry>
            <cylinder>
              <radius>0.25</radius>
              <length>0.7</length>
            </cylinder>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <cylinder>
              <radius>0.25</radius>
              <length>0.7</length>
            </cylinder>
          </geometry>
        </visual>
      </link>
    </model>

    <!-- LEFT BOX OBSTACLE -->

    <model name="left_box_obstacle">
      <static>true</static>
      <pose>-1.1 -0.8 0.35 0 0 0</pose>

      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.7 0.45 0.7</size>
            </box>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <box>
              <size>0.7 0.45 0.7</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>

    <!-- RIGHT BOX OBSTACLE -->

    <model name="right_box_obstacle">
      <static>true</static>
      <pose>0.8 0.5 0.35 0 0 0</pose>

      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 0.45 0.7</size>
            </box>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <box>
              <size>0.5 0.45 0.7</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>

    <!-- YELLOW CUBE TARGET -->

    <model name="yellow_cube">
      <static>true</static>
      <pose>0.7 -1.0 0.125 0 0 0</pose>

      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.25 0.25 0.25</size>
            </box>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <box>
              <size>0.25 0.25 0.25</size>
            </box>
          </geometry>

          <material>
            <ambient>1 1 0 1</ambient>
            <diffuse>1 1 0 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- RED CUBE FALSE TARGET -->

    <model name="red_cube">
      <static>true</static>
      <pose>0 -2.65 0.125 0 0 0</pose>

      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.25 0.25 0.25</size>
            </box>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <box>
              <size>0.25 0.25 0.25</size>
            </box>
          </geometry>

          <material>
            <ambient>1 0 0 1</ambient>
            <diffuse>1 0 0 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

  </world>

</sdf>