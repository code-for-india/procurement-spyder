angular.module('myApp').controller('SubscriptionController',
        function($scope, $location, Subscriptions) {

    $scope.lastPage = false;

    $scope.agriculture = [
      'Agricultural extension and research',
      'Animal production',
      'Crops',
      'Forestry',
      'General agriculture, fishing and forestry sector',
      'Irrigation and drainage',
    ]

    $scope.publicAdministration = [
      'Central government administration',
      'Compulsory health finance',
      // 'Compulsory pension and unemployment insurance',
      'General public administration sector',
      'Law and justice',
      // 'Public administration- Agriculture, fishing and forestry',
      'Public administration- Education',
      'Public administration- Energy and mining',
      'Public administration- Financial Sector',
      'Public administration- Health',
      'Public administration- Industry and trade',
      // 'Public administration- Information and communications',
      // 'Public administration- Other social services',
      'Public administration- Transportation',
      // 'Public administration- Water, sanitation and flood protection',
      'Sub-national government administration',
    ];

    $scope.information = [
    'General information and communications sector',
    'Information technology',
    'Telecommunications',
    ];

    $scope.education = [
      'Adult literacy/non-formal education',
      'General education sector',
      'Pre-primary education',
      'Primary education',
      'Secondary education',
      'Tertiary education',
      'Vocational training',
    ];

    $scope.finance = [
      'Banking',
      'Capital markets',
      'General finance sector',
      'Housing finance',
      'Non-compulsory health finance',
      'Non-compulsory pensions and insurance',
      'Payments, settlements, and remittance systems',
      'SME Finance',
      'Microfinance',
      'Other non-bank financial intermediaries',
      'Credit Reporting and Secured Transactions',
    ];

    $scope.health = [
      'Health',
      'Other social services',
    ];

    $scope.energyAndMining = [
      'Energy efficiency in power sector',
      'General energy sector',
      'Oil and gas',
      'Thermal Power Generation',
      'Large Hydropower',
      'Coal Mining',
      'Other Renewable Energy',
      'Other Mining and Extractive Industries',
      'Transmission and Distribution of Electricity',
    ];

    $scope.transportation = [
      'Aviation',
      'General transportation sector',
      'Ports, waterways and shipping',
      'Railways',
      'Urban Transport',
      'Rural and Inter-Urban Roads and Highways',
    ];

    $scope.waterSanitation = [
      'Flood protection',
      'General water, sanitation and flood protection',
      'Sanitation',
      'Solid waste management',
      'Water supply',
      'Wastewater Collection and Transportation',
      'Wastewater',
      'Treatment and Disposal',
    ];

    $scope.industryAndTrade = [
      'Agro-industry, marketing and trade',
      'General industry and trade sector',
      'Housing construction',
      'Other domestic and international trade',
      'Other industry',
      'Petrochemicals and fertilizers',
    ];

    // selected fruits
    $scope.selections = [];

    // toggle selections for a given fruit by name
    $scope.toggleSelection = function toggleSelection(category) {
      var idx = $scope.selections.indexOf(category);

      // is currently selected
      if (idx > -1) {
        $scope.selections.splice(idx, 1);
      }

      // is newly selected
      else {
        $scope.selections.push(category);
      }
    };

    $scope.states = [
      'All over India',
      "Andaman and Nicobar Islands",
      "Andhra Pradesh",
      "Arunachal Pradesh",
      "Assam",
      "Bihar",
      "Chandigarh",
      "Chhattisgarh",
      "Dadra and Nagar Haveli",
      "Daman and Diu",
      "Delhi",
      "Goa",
      "Gujarat",
      "Haryana",
      "Himachal Pradesh",
      "Jammu and Kashmir",
      "Jharkhand",
      "Karnataka",
      "Kerala",
      "Lakshadweep",
      "Madhya Pradesh",
      "Maharashtra",
      "Manipur",
      "Meghalaya",
      "Mizoram",
      "Nagaland",
      "Orissa",
      "Pondicherry",
      "Punjab",
      "Rajasthan",
      "Sikkim",
      "Tamil Nadu",
      "Tripura",
      "Uttaranchal",
      "Uttar Pradesh",
      "West Bengal"
    ];


    var subscription = $scope.subscription = {
        locations: [$scope.states[0]],
        fullname: '',
        email: ''
    };

    $scope.subscribe = function () {
      $scope.saving = true;
      subscription.sectors = $scope.selections;
      var subscriptionsResource = new Subscriptions(subscription);
      subscriptionsResource.$save().then(
        function (response) {
          if (response.updated) {
            return $location.path('/updated');
          }
          $location.path('/verify');
        },
        function (error) {
          alert((error.data && error.data.message) || 'Error! Please check the fields.');
        }
      ).finally(function() {
          $scope.saving = false;
      });
    }

    $scope.addLocation = function () {
      subscription.locations.push('');
    }

    $scope.removeLocation = function ($index) {
      subscription.locations.splice($index, 1);
    }

});
