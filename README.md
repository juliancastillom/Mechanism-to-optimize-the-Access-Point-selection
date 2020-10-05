# Mechanism to optimize the Access Point selection in an IoT environment based on SDN, multicriteria and group mobility
Mechanism to optimize the Access Point selection in an IoT environment based on SDN, multicriteria and group mobility

#### Files description
<table class="tg" style="undefined;table-layout: fixed; width: 2479px">
<colgroup>
<col style="width: 148px">
<col style="width: 447px">
<col style="width: 1884px">
</colgroup>
  <tr>
    <th class="tg-0pky">Directory</th>
    <th class="tg-0pky">Files</th>
    <th class="tg-0pky">Description</th>
  </tr>
  <tr>
    <td class="tg-0pky">DataSet-AP_selection</td>
    <td class="tg-0pky">* Devices_movement_Images_in_scenario_set-up<br>* dataset_escenario_set-up.png<br>* dataset_seleccion_parametros.csv<br>* devices_movement.csv</td>
    <td class="tg-0pky">This directory has the files that describe the movements that the devices make through the scenario in Mininet-WiFi; it also contains the initial dataset.</td>
  </tr>
  <tr>
    <td class="tg-0pky">Parameter_Selection</td>
    <td class="tg-0pky">* V1_HT_3-parametros(rssi-ocu-con).py<br>* V1_HT_4-parametros(rssi-ocu-con-dis).py<br>* V1_HT_4-parametros(rssi-ocu-con-pow).py<br>* V1_HT_5-parametros(rssi-ocu-con-pow).py<br>* V1_RF_Random_Forests_3(rssi-ocu-con)-parametros.py<br>* V1_RF_Random_Forests_4(rssi-ocu-con-dis)-parametros.py<br>* V1_RF_Random_Forests_4(rssi-ocu-con-pow)-parametros.py<br>* V1_RF_Random_Forests_5-parametros.py<br>* V1_SVM_3-parametros(rssi-ocu-con)_AP_Selection.py<br>* V1_SVM_4-parametros(rssi-ocu-con-dis)_AP_Selection.py<br>* V1_SVM_4-parametros(rssi-ocu-con-pow)_AP_Selection.py<br>* V1_SVM_5-parametros_AP_Selection.py<br>* dataset_seleccion_parametros.csv<br></td>
    <td class="tg-0pky">This directory has the files necessary to perform the analysis and processing the initial dataset to build the final dataset. Involves the following tasks: asses the quality of the dataset and reduces the dataset dimension, Identify and remove irrelevant or redundant features to reduce the dataset dimension.</td>
  </tr>
  <tr>
    <td class="tg-0pky">AP_Selection</td>
    <td class="tg-0pky">* ARF_Adaptive_Random_Forests.py<br>* HAT_Hoeffding_Adaptive_Tree.py<br>* HT_Hoeffding_Tree_or_Very_Fast_Decision_Tree.py<br>* RF_Random_Forest.py<br>* SVM_AP_Selection.py<br>* dataset_seleccion_ap.csv<br></td>
    <td class="tg-0pky">This directory has the files to train the machine learning algorithms (RF, ARF, HT, HAT, SVM) and later choose the most appropriate one.</td>
  </tr>
  <tr>
    <td class="tg-0pky">Group_mobility</td>
    <td class="tg-0pky">* Algoritmo_movilidad_grupo.pdf</td>
    <td class="tg-0pky">This directory has the flowchart of the group mobility algorithm that was implemented in Mininet-WiFi</td>
  </tr>
    <tr>
    <td class="tg-0pky">mininet_wifi</td>
    <td class="tg-0pky">* Modifications of the Mininet-WiFi source code</td>
    <td class="tg-0pky">This directory has the modifications of the Mininet-WiFi source code</td>
  </tr>
</table>
